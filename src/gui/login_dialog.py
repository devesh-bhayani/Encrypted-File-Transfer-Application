import sys
import os

# This is a temporary solution to allow running this script directly
# for testing. A better solution would be to have a separate test suite.
if __name__ == '__main__':
    # Add the project root to the python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)

from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from src.core.authentication import auth_manager
from src.database.user_manager import user_manager, UserRole

class RegistrationDialog(QDialog):
    """
    A dialog for new user registration.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Register New User")
        layout = QVBoxLayout(self)

        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.confirm_password_label = QLabel("Confirm Password:")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_input)

        self.register_button = QPushButton("Register")
        self.register_button.clicked.connect(self.handle_registration)
        layout.addWidget(self.register_button)

    def handle_registration(self):
        username = self.username_input.text()
        email = self.email_input.text()
        password = self.password_input.text()
        confirm_password = self.confirm_password_input.text()

        if not all([username, email, password, confirm_password]):
            QMessageBox.warning(self, "Registration Failed", "All fields are required.")
            return

        if password != confirm_password:
            QMessageBox.warning(self, "Registration Failed", "Passwords do not match.")
            return

        # Simple validation
        if len(password) < 8:
            QMessageBox.warning(self, "Registration Failed", "Password must be at least 8 characters long.")
            return

        user = user_manager.create_user(username, password, email)
        if user:
            QMessageBox.information(self, "Registration Successful", "You have successfully registered. Please log in.")
            self.accept()
        else:
            QMessageBox.warning(self, "Registration Failed", "Username or email may already be taken.")

class LoginDialog(QDialog):
    """
    A dialog for user login.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Login")
        self.user = None

        layout = QVBoxLayout(self)

        # Username
        self.username_label = QLabel("Username:")
        self.username_input = QLineEdit()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        # Password
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Buttons
        button_layout = QHBoxLayout()
        self.login_button = QPushButton("Login")
        self.register_button = QPushButton("Register")
        self.cancel_button = QPushButton("Cancel")
        button_layout.addWidget(self.login_button)
        button_layout.addWidget(self.register_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        # Connect signals
        self.login_button.clicked.connect(self.handle_login)
        self.register_button.clicked.connect(self.handle_register)
        self.cancel_button.clicked.connect(self.reject)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if auth_manager.login(username, password):
            self.user = auth_manager.get_current_user()
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
            
    def handle_register(self):
        reg_dialog = RegistrationDialog(self)
        reg_dialog.exec_()

    def get_user(self):
        return self.user

if __name__ == '__main__':
    # This is for testing the dialogs
    # In a real application, you would import these classes and use them
    app = QApplication(sys.argv)
    
    # Create a dummy admin user for testing if one doesn't exist
    if not user_manager.get_user_by_username('admin'):
        user_manager.create_user('admin', 'adminpassword', 'admin@example.com', role=UserRole.ADMIN)

    login_dialog = LoginDialog()
    if login_dialog.exec_() == QDialog.Accepted:
        print(f"Login successful for user: {login_dialog.get_user().username}")
        # Here you would open the main application window
        sys.exit(0)
    else:
        print("Login cancelled.")
        sys.exit(1)
