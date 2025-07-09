#!/usr/bin/env python3
"""
Unit tests for the user management module.
"""

import unittest
import os
import sys
import tempfile
import shutil
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add project root to path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.database.models import Base, User, UserRole

class TestUserManager(unittest.TestCase):
    """Test cases for the user management functionality."""
    
    def setUp(self):
        """Set up test fixtures with a temporary database."""
        # Create a temporary directory for test database
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, 'test_database.db')
        
        # Create a separate engine and session for testing
        self.engine = create_engine(f'sqlite:///{self.test_db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        
    def tearDown(self):
        """Clean up test fixtures."""
        # Clean up temporary database
        shutil.rmtree(self.temp_dir)
        
    def create_user(self, username, password, email, role=UserRole.USER):
        """Helper method to create a user for testing."""
        import bcrypt
        session = self.Session()
        try:
            # Check if user or email already exists
            if session.query(User).filter_by(username=username).first() is not None:
                return None
            if session.query(User).filter_by(email=email).first() is not None:
                return None

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
            return None
        finally:
            session.close()
    
    def authenticate_user(self, username, password):
        """Helper method to authenticate a user for testing."""
        import bcrypt
        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user
            return None
        finally:
            session.close()
            
    def get_user_by_username(self, username):
        """Helper method to get user by username for testing."""
        session = self.Session()
        try:
            return session.query(User).filter_by(username=username).first()
        finally:
            session.close()
            
    def get_user_by_id(self, user_id):
        """Helper method to get user by ID for testing."""
        session = self.Session()
        try:
            return session.query(User).filter_by(id=user_id).first()
        finally:
            session.close()
        
    def test_create_user(self):
        """Test user creation."""
        user = self.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.role, UserRole.USER)
        
    def test_create_admin_user(self):
        """Test admin user creation."""
        user = self.create_user(
            username="admin",
            password="adminpass123",
            email="admin@example.com",
            role=UserRole.ADMIN
        )
        
        self.assertIsNotNone(user)
        self.assertEqual(user.role, UserRole.ADMIN)
        
    def test_create_duplicate_user(self):
        """Test that duplicate usernames are not allowed."""
        # Create first user
        user1 = self.create_user(
            username="testuser",
            password="testpass123",
            email="test1@example.com"
        )
        self.assertIsNotNone(user1)
        
        # Try to create user with same username
        user2 = self.create_user(
            username="testuser",
            password="testpass456",
            email="test2@example.com"
        )
        self.assertIsNone(user2)
        
    def test_create_duplicate_email(self):
        """Test that duplicate emails are not allowed."""
        # Create first user
        user1 = self.create_user(
            username="testuser1",
            password="testpass123",
            email="test@example.com"
        )
        self.assertIsNotNone(user1)
        
        # Try to create user with same email
        user2 = self.create_user(
            username="testuser2",
            password="testpass456",
            email="test@example.com"
        )
        self.assertIsNone(user2)
        
    def test_authenticate_user(self):
        """Test user authentication."""
        # Create a user
        self.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        # Test successful authentication
        user = self.authenticate_user("testuser", "testpass123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "testuser")
        
        # Test failed authentication with wrong password
        user = self.authenticate_user("testuser", "wrongpass")
        self.assertIsNone(user)
        
        # Test failed authentication with wrong username
        user = self.authenticate_user("wronguser", "testpass123")
        self.assertIsNone(user)
        
    def test_get_user_by_username(self):
        """Test retrieving user by username."""
        # Create a user
        created_user = self.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        # Retrieve the user
        retrieved_user = self.get_user_by_username("testuser")
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.id, created_user.id)
        self.assertEqual(retrieved_user.username, "testuser")
        
        # Try to retrieve non-existent user
        non_existent_user = self.get_user_by_username("nonexistent")
        self.assertIsNone(non_existent_user)
        
    def test_get_user_by_id(self):
        """Test retrieving user by ID."""
        # Create a user
        created_user = self.create_user(
            username="testuser",
            password="testpass123",
            email="test@example.com"
        )
        
        # Retrieve the user by ID
        retrieved_user = self.get_user_by_id(created_user.id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.username, "testuser")
        
        # Try to retrieve non-existent user
        non_existent_user = self.get_user_by_id(99999)
        self.assertIsNone(non_existent_user)

if __name__ == '__main__':
    unittest.main() 