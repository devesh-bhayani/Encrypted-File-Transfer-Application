from ..database.user_manager import user_manager
from ..database.audit_logger import audit_logger

class AuthenticationManager:
    """
    Handles user authentication and session management.
    """
    def __init__(self):
        self.current_user = None

    def login(self, username, password):
        """
        Logs a user in.

        :param username: The username to authenticate.
        :param password: The password to authenticate.
        :return: True if login is successful, False otherwise.
        """
        user = user_manager.authenticate_user(username, password)
        if user:
            self.current_user = user
            audit_logger.log_event(
                action="User Login",
                user_id=user.id,
                details=f"User '{username}' logged in successfully."
            )
            return True
        else:
            audit_logger.log_event(
                action="Failed Login Attempt",
                details=f"Failed login attempt for username '{username}'."
            )
            return False

    def logout(self):
        """
        Logs the current user out.
        """
        if self.current_user:
            audit_logger.log_event(
                action="User Logout",
                user_id=self.current_user.id,
                details=f"User '{self.current_user.username}' logged out."
            )
            self.current_user = None

    def get_current_user(self):
        """
        Returns the currently authenticated user.

        :return: The User object or None if no user is logged in.
        """
        return self.current_user

    def is_authenticated(self):
        """
        Checks if a user is currently authenticated.

        :return: True if a user is logged in, False otherwise.
        """
        return self.current_user is not None

# Instantiate a single authentication manager for the application
auth_manager = AuthenticationManager()
