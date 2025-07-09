import socket
import threading
import os
import json
import tempfile
from .encryption import encryption_manager
from ..database.audit_logger import audit_logger

class FileTransferServer:
    """
    A server to receive files over a TCP socket.
    """
    def __init__(self, host='0.0.0.0', port=9999):
        self.host = host
        self.port = port
        self.server_socket = None
        self.running = False

    def start(self, progress_callback=None):
        """Starts the server to listen for incoming connections."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        self.running = True
        audit_logger.log_event("Server Started", details=f"Listening on {self.host}:{self.port}")

        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                audit_logger.log_event("Connection Accepted", details=f"Connection from {addr}")
                handler_thread = threading.Thread(target=self._handle_client, args=(client_socket, progress_callback))
                handler_thread.start()
            except OSError:
                # This can happen when the socket is closed while accept() is blocking
                break

    def stop(self):
        """Stops the server."""
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        audit_logger.log_event("Server Stopped")

    def _handle_client(self, client_socket, progress_callback):
        """Handles a single client connection."""
        try:
            # Receive metadata
            header_data = b""
            while b'\\n\\n' not in header_data:
                header_data += client_socket.recv(1)
            
            metadata_str = header_data.split(b'\\n\\n', 1)[0].decode('utf-8')
            metadata = json.loads(metadata_str)
            file_name = metadata.get('file_name')
            file_size = metadata.get('file_size')

            # For simplicity, save to a 'downloads' directory
            download_dir = 'downloads'
            if not os.path.exists(download_dir):
                os.makedirs(download_dir)
            file_path = os.path.join(download_dir, os.path.basename(file_name))

            with open(file_path, 'wb') as f:
                bytes_received = 0
                while bytes_received < file_size:
                    chunk = client_socket.recv(4096)
                    if not chunk:
                        break
                    f.write(chunk)
                    bytes_received += len(chunk)
                    if progress_callback:
                        progress_callback(file_name, bytes_received, file_size)
            
            audit_logger.log_event("File Received", details=f"Received {file_name} ({file_size} bytes)")

        except Exception as e:
            audit_logger.log_event("Server Error", details=f"Error handling client: {e}")
        finally:
            client_socket.close()

class FileTransferClient:
    """
    A client to send files over a TCP socket.
    """
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send_file(self, file_path, password, progress_callback=None):
        """
        Encrypts and sends a file to the server.

        :param file_path: The path to the file to send.
        :param password: The password for encryption.
        :param progress_callback: A function to call with progress updates.
        """
        temp_dir = tempfile.gettempdir()
        encrypted_file_path = None
        try:
            # 1. Encrypt the file
            encrypted_file_path = encryption_manager.encrypt_file(file_path, password, os.path.join(temp_dir, os.path.basename(file_path) + ".enc"))

            # 2. Send the encrypted file
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self.host, self.port))

            file_name = os.path.basename(encrypted_file_path)
            file_size = os.path.getsize(encrypted_file_path)
            
            # Send metadata header
            metadata = {'file_name': file_name, 'file_size': file_size}
            header = json.dumps(metadata).encode('utf-8') + b'\\n\\n'
            client_socket.sendall(header)

            with open(encrypted_file_path, 'rb') as f:
                bytes_sent = 0
                while chunk := f.read(4096):
                    client_socket.sendall(chunk)
                    bytes_sent += len(chunk)
                    if progress_callback:
                        progress_callback(os.path.basename(file_path), bytes_sent, file_size)

            audit_logger.log_event("File Sent", details=f"Sent {file_name} to {self.host}:{self.port}")

        except Exception as e:
            audit_logger.log_event("Client Error", details=f"Error sending file: {e}")
        finally:
            if 'client_socket' in locals() and client_socket:
                client_socket.close()
            # Clean up the temporary encrypted file
            if encrypted_file_path and os.path.exists(encrypted_file_path):
                os.remove(encrypted_file_path)
