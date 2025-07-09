#!/usr/bin/env python3
"""
Unit tests for the encryption module.
"""

import unittest
import os
import tempfile
import sys

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.core.encryption import encryption_manager

class TestEncryption(unittest.TestCase):
    """Test cases for the encryption functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.test_data = b"This is a test file content for encryption testing."
        self.password = "test_password_123"
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary files
        for file in os.listdir(self.temp_dir):
            os.remove(os.path.join(self.temp_dir, file))
        os.rmdir(self.temp_dir)
        
    def test_encrypt_decrypt_file(self):
        """Test file encryption and decryption."""
        # Create a test file
        test_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(test_file, 'wb') as f:
            f.write(self.test_data)
            
        # Encrypt the file
        encrypted_file = encryption_manager.encrypt_file(test_file, self.password)
        self.assertTrue(os.path.exists(encrypted_file))
        self.assertTrue(encrypted_file.endswith('.enc'))
        
        # Verify encrypted file is different from original
        with open(encrypted_file, 'rb') as f:
            encrypted_data = f.read()
        self.assertNotEqual(self.test_data, encrypted_data)
        
        # Decrypt the file
        decrypted_file = encryption_manager.decrypt_file(encrypted_file, self.password)
        self.assertTrue(os.path.exists(decrypted_file))
        
        # Verify decrypted content matches original
        with open(decrypted_file, 'rb') as f:
            decrypted_data = f.read()
        self.assertEqual(self.test_data, decrypted_data)
        
    def test_decrypt_with_wrong_password(self):
        """Test decryption with incorrect password."""
        # Create and encrypt a test file
        test_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(test_file, 'wb') as f:
            f.write(self.test_data)
            
        encrypted_file = encryption_manager.encrypt_file(test_file, self.password)
        
        # Try to decrypt with wrong password
        decrypted_file = encryption_manager.decrypt_file(encrypted_file, "wrong_password")
        self.assertIsNone(decrypted_file)  # Should return None on failure
        
    def test_encrypt_empty_file(self):
        """Test encryption of an empty file."""
        # Create an empty test file
        test_file = os.path.join(self.temp_dir, "empty_file.txt")
        with open(test_file, 'wb') as f:
            pass  # Create empty file
            
        # Encrypt the empty file
        encrypted_file = encryption_manager.encrypt_file(test_file, self.password)
        self.assertTrue(os.path.exists(encrypted_file))
        
        # Decrypt the file
        decrypted_file = encryption_manager.decrypt_file(encrypted_file, self.password)
        self.assertTrue(os.path.exists(decrypted_file))
        
        # Verify decrypted file is empty
        with open(decrypted_file, 'rb') as f:
            decrypted_data = f.read()
        self.assertEqual(b"", decrypted_data)

if __name__ == '__main__':
    unittest.main() 