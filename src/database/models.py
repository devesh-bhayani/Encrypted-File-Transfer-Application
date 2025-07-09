import datetime
import enum
import os
import sys
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# This is a temporary solution to allow running this script directly
# for database creation. A better solution would be to use a migration
# tool like Alembic.
if __name__ == '__main__':
    # Add the project root to the python path
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    sys.path.insert(0, project_root)

from src.utils.config import config

# Get DB config
db_config = config.get_db_config()
db_path = db_config.get('path')

# Create an engine that stores data in the local directory's
# The full path to the database file is now used
engine = create_engine(f'sqlite:///{db_path}')

# Create a configured "Session" class
Session = sessionmaker(bind=engine)

# Create a Session
session = Session()

Base = declarative_base()

class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"<User(username='{self.username}', email='{self.email}', role='{self.role.value}')>"

class AuditLog(Base):
    __tablename__ = 'audit_logs'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    action = Column(String(100), nullable=False)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<AuditLog(user_id={self.user_id}, action='{self.action}', timestamp='{self.timestamp}')>"

class TransferHistory(Base):
    __tablename__ = 'transfer_history'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<TransferHistory(file_name='{self.file_name}', status='{self.status}')>"

def create_db():
    """Creates the database and tables."""
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    # This will create the database file and tables when the script is run directly
    create_db()
    print("Database and tables created successfully.")
