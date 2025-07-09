import bcrypt
from sqlalchemy.orm import sessionmaker
from .models import User, UserRole, engine

class UserManager:
    """
    Handles user management operations such as creation, authentication, and retrieval.
    """
    def __init__(self):
        self.Session = sessionmaker(bind=engine)

    def create_user(self, username, password, email, role=UserRole.USER):
        """
        Creates a new user with a hashed password.

        :param username: The user's username.
        :param password: The user's plain-text password.
        :param email: The user's email address.
        :param role: The user's role (admin or user).
        :return: The created User object or None if user/email already exists.
        """
        session = self.Session()
        try:
            # Check if user or email already exists
            if session.query(User).filter_by(username=username).first() is not None:
                return None  # Username already exists
            if session.query(User).filter_by(email=email).first() is not None:
                return None  # Email already exists

            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Create new user
            new_user = User(
                username=username,
                password_hash=hashed_password.decode('utf-8'),
                email=email,
                role=role
            )
            session.add(new_user)
            session.commit()
            return new_user
        except Exception as e:
            session.rollback()
            # In a real app, you'd want to log this error
            print(f"Error creating user: {e}")
            return None
        finally:
            session.close()

    def authenticate_user(self, username, password):
        """
        Authenticates a user by checking their username and password.

        :param username: The user's username.
        :param password: The user's plain-text password.
        :return: The User object if authentication is successful, otherwise None.
        """
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user
            return None
        finally:
            session.close()

    def get_user_by_username(self, username):
        """
        Retrieves a user by their username.

        :param username: The username to search for.
        :return: The User object or None if not found.
        """
        session = self.Session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()

    def get_user_by_id(self, user_id):
        """
        Retrieves a user by their ID.

        :param user_id: The ID of the user.
        :return: The User object or None if not found.
        """
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()

# Instantiate a single user manager for the application
user_manager = UserManager()
