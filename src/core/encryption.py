import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.backends import default_backend
from ..utils.config import config

class EncryptionManager:
    """
    Handles file encryption and decryption using AES-256 in GCM mode.
    """
    def __init__(self):
        enc_config = config.get_encryption_config()
        self.key_size = enc_config.get('key_size', 32)
        self.iv_size = 12  # GCM recommended IV size is 12 bytes
        self.salt_size = enc_config.get('salt_size', 16)
        self.iterations = enc_config.get('iterations', 100000)
        self.chunk_size = 64 * 1024  # 64KB
        self.tag_size = 16  # GCM tag size is always 16 bytes

    def _derive_key(self, password, salt):
        """Derives a key from a password and salt using PBKDF2."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_size,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        return kdf.derive(password.encode('utf-8'))

    def encrypt_file(self, file_path, password, output_path=None):
        """
        Encrypts a file and prepends the salt, IV, and appends the auth tag.

        :param file_path: Path to the file to encrypt.
        :param password: The password to use for key derivation.
        :param output_path: Path to write the encrypted file to. If None, it will be file_path + '.enc'.
        :return: The path to the encrypted file.
        """
        if not output_path:
            output_path = file_path + '.enc'

        salt = os.urandom(self.salt_size)
        iv = os.urandom(self.iv_size)
        key = self._derive_key(password, salt)

        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv),
            backend=default_backend()
        ).encryptor()

        with open(file_path, 'rb') as f_in, open(output_path, 'wb') as f_out:
            # Write salt and IV to the output file first
            f_out.write(salt)
            f_out.write(iv)

            while chunk := f_in.read(self.chunk_size):
                encrypted_chunk = encryptor.update(chunk)
                f_out.write(encrypted_chunk)

            # Finalize encryption and get the auth tag
            encryptor.finalize()
            f_out.write(encryptor.tag)
        
        return output_path

    def decrypt_file(self, file_path, password, output_path=None):
        """
        Decrypts a file that was encrypted with encrypt_file.

        :param file_path: Path to the encrypted file.
        :param password: The password to use for key derivation.
        :param output_path: Path to write the decrypted file to. If None, it will be file_path without '.enc'.
        :return: The path to the decrypted file, or None if decryption fails.
        """
        if not output_path:
            if file_path.endswith('.enc'):
                output_path = file_path[:-4]
            else:
                output_path = file_path + '.dec'

        try:
            with open(file_path, 'rb') as f_in:
                # Read metadata
                salt = f_in.read(self.salt_size)
                iv = f_in.read(self.iv_size)
                
                # Read the encrypted content and tag
                encrypted_content = f_in.read()
                
                # The last 16 bytes are the authentication tag
                if len(encrypted_content) < self.tag_size:
                    raise ValueError("File too short to contain valid encrypted data")
                    
                tag = encrypted_content[-self.tag_size:]
                encrypted_data = encrypted_content[:-self.tag_size]
                
                key = self._derive_key(password, salt)

                decryptor = Cipher(
                    algorithms.AES(key),
                    modes.GCM(iv, tag),
                    backend=default_backend()
                ).decryptor()

                with open(output_path, 'wb') as f_out:
                    # Decrypt in chunks
                    for i in range(0, len(encrypted_data), self.chunk_size):
                        chunk = encrypted_data[i:i + self.chunk_size]
                        decrypted_chunk = decryptor.update(chunk)
                        f_out.write(decrypted_chunk)
                    
                    # Finalize decryption (this will verify the authentication tag)
                    decryptor.finalize()
                    
                return output_path
                
        except Exception as e:
            # Clean up partial file if it exists
            if os.path.exists(output_path):
                os.remove(output_path)
            print(f"Decryption failed: {e}")
            return None

# Instantiate a single encryption manager for the application
encryption_manager = EncryptionManager()
