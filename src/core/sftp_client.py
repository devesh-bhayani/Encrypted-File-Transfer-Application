import paramiko
import os
from ..database.audit_logger import audit_logger

class SFTPClient:
    """
    A client for transferring files using the SFTP protocol.
    """
    def __init__(self, hostname, port, username, password=None, private_key_path=None):
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password
        self.private_key_path = private_key_path
        self.sftp = None
        self.transport = None

    def connect(self):
        """
        Connects to the SFTP server.
        """
        try:
            self.transport = paramiko.Transport((self.hostname, self.port))
            
            if self.private_key_path:
                private_key = paramiko.RSAKey(filename=self.private_key_path)
                self.transport.connect(username=self.username, pkey=private_key)
            elif self.password:
                self.transport.connect(username=self.username, password=self.password)
            else:
                raise Exception("Either password or private key must be provided.")

            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
            audit_logger.log_event("SFTP Connected", details=f"Connected to {self.hostname}")
            return True
        except Exception as e:
            audit_logger.log_event("SFTP Connection Failed", details=f"Failed to connect to {self.hostname}: {e}")
            return False

    def disconnect(self):
        """
        Closes the SFTP connection.
        """
        if self.sftp:
            self.sftp.close()
        if self.transport:
            self.transport.close()
        audit_logger.log_event("SFTP Disconnected", details=f"Disconnected from {self.hostname}")

    def upload_file(self, local_path, remote_path, progress_callback=None):
        """
        Uploads a file to the SFTP server.

        :param local_path: The local path of the file to upload.
        :param remote_path: The remote path to store the file.
        :param progress_callback: A function to call with progress updates.
        """
        if not self.sftp:
            raise Exception("Not connected to SFTP server.")
        
        try:
            file_size = os.path.getsize(local_path)
            self.sftp.put(local_path, remote_path, callback=lambda sent, total: progress_callback(os.path.basename(local_path), sent, file_size) if progress_callback else None)
            audit_logger.log_event("SFTP File Uploaded", details=f"Uploaded {local_path} to {remote_path}")
            return True
        except Exception as e:
            audit_logger.log_event("SFTP Upload Failed", details=f"Failed to upload {local_path}: {e}")
            return False

    def download_file(self, remote_path, local_path, progress_callback=None):
        """
        Downloads a file from the SFTP server.

        :param remote_path: The remote path of the file to download.
        :param local_path: The local path to store the downloaded file.
        :param progress_callback: A function to call with progress updates.
        """
        if not self.sftp:
            raise Exception("Not connected to SFTP server.")

        try:
            file_size = self.sftp.stat(remote_path).st_size
            self.sftp.get(remote_path, local_path, callback=lambda received, total: progress_callback(os.path.basename(remote_path), received, file_size) if progress_callback else None)
            audit_logger.log_event("SFTP File Downloaded", details=f"Downloaded {remote_path} to {local_path}")
            return True
        except Exception as e:
            audit_logger.log_event("SFTP Download Failed", details=f"Failed to download {remote_path}: {e}")
            return False

    def list_dir(self, remote_path):
        """
        Lists the contents of a remote directory.

        :param remote_path: The path of the remote directory.
        :return: A list of directory contents.
        """
        if not self.sftp:
            raise Exception("Not connected to SFTP server.")
        
        return self.sftp.listdir(remote_path)
