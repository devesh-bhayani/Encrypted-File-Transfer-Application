import sys
import os
import time
import threading
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QSplitter, QTabWidget, QLabel, QPushButton, 
                             QLineEdit, QTextEdit, QGroupBox, QMessageBox,
                             QApplication, QMenuBar, QAction, QStatusBar,
                             QInputDialog, QFileDialog)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal, QObject

# Add project root to path for testing
if __name__ == '__main__':
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)

from src.gui.login_dialog import LoginDialog
from src.gui.file_browser import FileBrowser
from src.gui.transfer_progress import TransferProgressWidget
from src.core.file_transfer import FileTransferClient, FileTransferServer
from src.core.sftp_client import SFTPClient
from src.core.authentication import auth_manager
from src.database.audit_logger import audit_logger
from src.core.encryption import encryption_manager

class TransferWorker(QObject):
    """Worker class for handling file transfers in a separate thread."""
    progress_updated = pyqtSignal(str, int, int)  # file_name, bytes_transferred, total_size
    transfer_complete = pyqtSignal()
    transfer_error = pyqtSignal(str)
    
    def __init__(self, transfer_type, **kwargs):
        super().__init__()
        self.transfer_type = transfer_type
        self.kwargs = kwargs
        
    def run(self):
        """Runs the file transfer operation."""
        try:
            if self.transfer_type == 'socket':
                client = FileTransferClient(self.kwargs['host'], self.kwargs['port'])
                client.send_file(
                    self.kwargs['file_path'], 
                    self.kwargs['password'],
                    progress_callback=self.progress_updated.emit
                )
            elif self.transfer_type == 'sftp':
                client = SFTPClient(
                    self.kwargs['hostname'],
                    self.kwargs['port'],
                    self.kwargs['username'],
                    self.kwargs['password']
                )
                if client.connect():
                    client.upload_file(
                        self.kwargs['local_path'],
                        self.kwargs['remote_path'],
                        progress_callback=self.progress_updated.emit
                    )
                    client.disconnect()
                else:
                    self.transfer_error.emit("Failed to connect to SFTP server")
                    return
            
            self.transfer_complete.emit()
            
        except Exception as e:
            self.transfer_error.emit(str(e))

class MainWindow(QMainWindow):
    """
    The main application window.
    """
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.server = None
        self.server_thread = None
        self.setup_ui()
        self.setup_menu()
        self.setup_status_bar()
        
    def setup_ui(self):
        """Sets up the main user interface."""
        self.setWindowTitle("Encrypted File Transfer Application")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter)
        
        # Left panel - File browser
        self.file_browser = FileBrowser()
        splitter.addWidget(self.file_browser)
        
        # Right panel - Transfer controls and progress
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)
        
        # Transfer controls
        self.setup_transfer_controls(right_layout)
        
        # File Utilities
        self.setup_utilities(right_layout)

        # Progress widget
        self.progress_widget = TransferProgressWidget()
        self.progress_widget.cancel_requested.connect(self.cancel_transfer)
        right_layout.addWidget(self.progress_widget)
        
        # Log area
        log_group = QGroupBox("Activity Log")
        log_layout = QVBoxLayout(log_group)
        self.log_text = QTextEdit()
        self.log_text.setMaximumHeight(200)
        self.log_text.setReadOnly(True)
        log_layout.addWidget(self.log_text)
        right_layout.addWidget(log_group)
        
        splitter.addWidget(right_panel)
        
        # Set splitter proportions
        splitter.setSizes([400, 800])
        
    def setup_transfer_controls(self, layout):
        """Sets up the transfer control widgets."""
        # Socket transfer group
        socket_group = QGroupBox("Socket Transfer")
        socket_layout = QVBoxLayout(socket_group)
        
        # Host and port
        host_layout = QHBoxLayout()
        host_layout.addWidget(QLabel("Host:"))
        self.host_input = QLineEdit("localhost")
        host_layout.addWidget(self.host_input)
        host_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit("9999")
        host_layout.addWidget(self.port_input)
        socket_layout.addLayout(host_layout)
        
        # Transfer buttons
        socket_btn_layout = QHBoxLayout()
        self.send_socket_btn = QPushButton("Send File")
        self.send_socket_btn.clicked.connect(self.send_file_socket)
        socket_btn_layout.addWidget(self.send_socket_btn)
        
        self.start_server_btn = QPushButton("Start Server")
        self.start_server_btn.clicked.connect(self.toggle_server)
        socket_btn_layout.addWidget(self.start_server_btn)
        
        socket_layout.addLayout(socket_btn_layout)
        layout.addWidget(socket_group)
        
        # SFTP transfer group
        sftp_group = QGroupBox("SFTP Transfer")
        sftp_layout = QVBoxLayout(sftp_group)
        
        # SFTP connection details
        sftp_conn_layout = QHBoxLayout()
        sftp_conn_layout.addWidget(QLabel("Host:"))
        self.sftp_host_input = QLineEdit()
        sftp_conn_layout.addWidget(self.sftp_host_input)
        sftp_conn_layout.addWidget(QLabel("Port:"))
        self.sftp_port_input = QLineEdit("22")
        sftp_conn_layout.addWidget(self.sftp_port_input)
        sftp_layout.addLayout(sftp_conn_layout)
        
        sftp_auth_layout = QHBoxLayout()
        sftp_auth_layout.addWidget(QLabel("Username:"))
        self.sftp_username_input = QLineEdit()
        sftp_auth_layout.addWidget(self.sftp_username_input)
        sftp_auth_layout.addWidget(QLabel("Password:"))
        self.sftp_password_input = QLineEdit()
        self.sftp_password_input.setEchoMode(QLineEdit.Password)
        sftp_auth_layout.addWidget(self.sftp_password_input)
        sftp_layout.addLayout(sftp_auth_layout)
        
        # Remote path
        remote_path_layout = QHBoxLayout()
        remote_path_layout.addWidget(QLabel("Remote Path:"))
        self.remote_path_input = QLineEdit()
        remote_path_layout.addWidget(self.remote_path_input)
        sftp_layout.addLayout(remote_path_layout)
        
        # SFTP transfer button
        self.send_sftp_btn = QPushButton("Send File via SFTP")
        self.send_sftp_btn.clicked.connect(self.send_file_sftp)
        sftp_layout.addWidget(self.send_sftp_btn)
        
        layout.addWidget(sftp_group)
        
    def setup_utilities(self, layout):
        """Sets up the file utility widgets."""
        util_group = QGroupBox("File Utilities")
        util_layout = QVBoxLayout(util_group)
        
        self.decrypt_btn = QPushButton("Decrypt File")
        self.decrypt_btn.clicked.connect(self.decrypt_file_local)
        util_layout.addWidget(self.decrypt_btn)
        
        layout.addWidget(util_group)

    def setup_menu(self):
        """Sets up the application menu."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        logout_action = QAction('Logout', self)
        logout_action.triggered.connect(self.logout)
        file_menu.addAction(logout_action)
        
        exit_action = QAction('Exit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
        
    def setup_status_bar(self):
        """Sets up the status bar."""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
    def show_login(self):
        """Shows the login dialog."""
        login_dialog = LoginDialog(self)
        if login_dialog.exec_() == LoginDialog.Accepted:
            self.current_user = login_dialog.get_user()
            self.log_message(f"Welcome, {self.current_user.username}!")
            self.status_bar.showMessage(f"Logged in as: {self.current_user.username}")
            return True
        return False
        
    def logout(self):
        """Logs out the current user."""
        if self.current_user:
            auth_manager.logout()
            self.current_user = None
            self.log_message("Logged out successfully.")
            self.status_bar.showMessage("Not logged in")
            self.close()
            
    def send_file_socket(self):
        """Sends a file using socket transfer."""
        file_path = self.file_browser.get_selected_file_path()
        if not file_path or not os.path.isfile(file_path):
            QMessageBox.warning(self, "Error", "Please select a file to send.")
            return
            
        # Get encryption password
        password, ok = QInputDialog.getText(self, "Encryption Password", 
                                          "Enter password for file encryption:", 
                                          QLineEdit.Password)
        if not ok or not password:
            return
            
        # Start transfer in separate thread
        self.start_transfer('socket', {
            'host': self.host_input.text(),
            'port': int(self.port_input.text()),
            'file_path': file_path,
            'password': password
        })
        
    def send_file_sftp(self):
        """Sends a file using SFTP transfer."""
        file_path = self.file_browser.get_selected_file_path()
        if not file_path or not os.path.isfile(file_path):
            QMessageBox.warning(self, "Error", "Please select a file to send.")
            return
            
        if not all([self.sftp_host_input.text(), self.sftp_username_input.text(), 
                   self.sftp_password_input.text(), self.remote_path_input.text()]):
            QMessageBox.warning(self, "Error", "Please fill in all SFTP connection details.")
            return
            
        # Start transfer in separate thread
        self.start_transfer('sftp', {
            'hostname': self.sftp_host_input.text(),
            'port': int(self.sftp_port_input.text()),
            'username': self.sftp_username_input.text(),
            'password': self.sftp_password_input.text(),
            'local_path': file_path,
            'remote_path': self.remote_path_input.text()
        })
        
    def start_transfer(self, transfer_type, kwargs):
        """Starts a file transfer operation."""
        self.worker = TransferWorker(transfer_type, **kwargs)
        self.worker_thread = threading.Thread(target=self.worker.run)
        
        # Connect signals
        self.worker.progress_updated.connect(self.progress_widget.update_progress)
        self.worker.transfer_complete.connect(self.on_transfer_complete)
        self.worker.transfer_error.connect(self.on_transfer_error)
        
        self.worker_thread.start()
        self.log_message(f"Started {transfer_type} transfer...")
        
    def decrypt_file_local(self):
        """Decrypts a locally selected file."""
        # Open file dialog to select an encrypted file
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Encrypted File", "", 
                                                   "Encrypted Files (*.enc);;All Files (*)", options=options)
        if not file_path:
            return

        # Get decryption password
        password, ok = QInputDialog.getText(self, "Decryption Password",
                                          "Enter password for file decryption:",
                                          QLineEdit.Password)
        if not ok or not password:
            return
            
        # Get output path
        output_path, _ = QFileDialog.getSaveFileName(self, "Save Decrypted File", os.path.basename(file_path).replace('.enc', ''))
        if not output_path:
            return

        # Decrypt the file
        try:
            decrypted_file = encryption_manager.decrypt_file(file_path, password, output_path)
            if decrypted_file:
                self.log_message(f"Successfully decrypted '{os.path.basename(file_path)}' to '{os.path.basename(output_path)}'")
                QMessageBox.information(self, "Success", "File decrypted successfully!")
            else:
                self.log_message(f"Failed to decrypt '{os.path.basename(file_path)}'. Check password or file integrity.")
                QMessageBox.critical(self, "Decryption Failed", "Failed to decrypt the file. The password may be incorrect or the file may be corrupt.")
        except Exception as e:
            self.log_message(f"An error occurred during decryption: {e}")
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def on_transfer_complete(self):
        """Handles transfer completion."""
        self.progress_widget.transfer_complete()
        self.log_message("Transfer completed successfully!")
        
    def on_transfer_error(self, error_msg):
        """Handles transfer errors."""
        self.log_message(f"Transfer failed: {error_msg}")
        QMessageBox.critical(self, "Transfer Error", f"Transfer failed: {error_msg}")
        
    def cancel_transfer(self):
        """Cancels the current transfer."""
        # Note: This is a simplified implementation
        # In a real application, you'd need proper thread cancellation
        self.log_message("Transfer cancelled by user.")
        
    def toggle_server(self):
        """Starts or stops the file transfer server."""
        if self.server is None:
            self.server = FileTransferServer(port=int(self.port_input.text()))
            self.server_thread = threading.Thread(target=self.server.start)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.start_server_btn.setText("Stop Server")
            self.log_message(f"Server started on port {self.port_input.text()}")
        else:
            self.server.stop()
            self.server = None
            self.server_thread = None
            self.start_server_btn.setText("Start Server")
            self.log_message("Server stopped")
            
    def log_message(self, message):
        """Adds a message to the activity log."""
        self.log_text.append(f"[{time.strftime('%H:%M:%S')}] {message}")
        
    def show_about(self):
        """Shows the about dialog."""
        QMessageBox.about(self, "About", 
                         "Encrypted File Transfer Application\n\n"
                         "A secure file transfer application with AES encryption\n"
                         "and support for both socket and SFTP protocols.")
        
    def closeEvent(self, event):
        """Handles the window close event."""
        if self.server:
            self.server.stop()
        event.accept()

if __name__ == '__main__':
    import time
    
    app = QApplication(sys.argv)
    
    # Create main window
    main_window = MainWindow()
    
    # Show login dialog first
    if main_window.show_login():
        main_window.show()
        sys.exit(app.exec_())
    else:
        sys.exit(0)
