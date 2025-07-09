# Encrypted File Transfer Application - Developer Guide

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Database Schema](#database-schema)
5. [Security Implementation](#security-implementation)
6. [API Reference](#api-reference)
7. [Development Setup](#development-setup)
8. [Testing](#testing)
9. [Extending the Application](#extending-the-application)
10. [Deployment](#deployment)

## Architecture Overview

The Encrypted File Transfer Application follows a modular, layered architecture designed for security, maintainability, and extensibility.

### Architecture Layers

```
┌─────────────────────────────────────┐
│           GUI Layer                 │
│  (PyQt5 - User Interface)          │
├─────────────────────────────────────┤
│           Core Layer                │
│  (Business Logic & Encryption)     │
├─────────────────────────────────────┤
│         Database Layer              │
│  (SQLAlchemy - Data Persistence)   │
├─────────────────────────────────────┤
│          Utils Layer                │
│  (Configuration & Logging)         │
└─────────────────────────────────────┘
```

### Design Principles

- **Separation of Concerns**: Each module has a specific responsibility
- **Security by Design**: Encryption and security are built into the core
- **Modularity**: Components can be modified or replaced independently
- **Testability**: Code is structured to facilitate unit testing
- **Configuration-Driven**: Behavior can be modified through configuration

## Project Structure

```
encrypted_file_transfer/
├── src/                          # Main source code
│   ├── core/                     # Core business logic
│   │   ├── __init__.py
│   │   ├── encryption.py         # AES encryption implementation
│   │   ├── file_transfer.py      # Socket-based file transfer
│   │   ├── sftp_client.py        # SFTP protocol implementation
│   │   └── authentication.py     # User authentication
│   ├── gui/                      # User interface components
│   │   ├── __init__.py
│   │   ├── main_window.py        # Main application window
│   │   ├── login_dialog.py       # Login and registration dialogs
│   │   ├── transfer_progress.py  # Progress monitoring widget
│   │   └── file_browser.py       # File system browser
│   ├── database/                 # Data persistence layer
│   │   ├── __init__.py
│   │   ├── models.py             # SQLAlchemy models
│   │   ├── user_manager.py       # User management operations
│   │   └── audit_logger.py       # Audit logging functionality
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py             # Configuration management
│   │   ├── logger.py             # Logging setup
│   │   └── helpers.py            # Helper functions
│   └── main.py                   # Application entry point
├── config/                       # Configuration files
│   ├── settings.json             # Application settings
│   ├── encryption_config.json    # Encryption parameters
│   └── database.db              # SQLite database
├── tests/                        # Unit and integration tests
│   ├── test_encryption.py        # Encryption tests
│   ├── test_user_manager.py      # User management tests
│   └── run_tests.py              # Test runner
├── docs/                         # Documentation
│   ├── user_guide.md             # User documentation
│   ├── developer_guide.md        # This file
│   └── admin_guide.md            # Administrator documentation
├── logs/                         # Application logs
├── downloads/                    # Default download directory
├── requirements.txt              # Python dependencies
└── README.md                     # Project overview
```

## Core Components

### Encryption Module (`src/core/encryption.py`)

Implements AES-256-GCM encryption for secure file transfer.

```python
class EncryptionManager:
    def __init__(self):
        # Configuration from encryption_config.json
        self.key_size = 32      # AES-256
        self.iv_size = 12       # GCM recommended
        self.salt_size = 16     # PBKDF2 salt
        self.iterations = 100000 # Key derivation iterations
        
    def encrypt_file(self, file_path, password, output_path=None):
        # Encrypts file with AES-256-GCM
        
    def decrypt_file(self, file_path, password, output_path=None):
        # Decrypts file and verifies authentication tag
```

**Key Features:**
- PBKDF2 key derivation with 100,000 iterations
- Unique salt and IV for each encryption operation
- Authentication tag verification for integrity
- Chunked processing for large files

### File Transfer Module (`src/core/file_transfer.py`)

Implements custom socket-based file transfer protocol.

```python
class FileTransferServer:
    def start(self, progress_callback=None):
        # Starts TCP server to receive files
        
    def _handle_client(self, client_socket, progress_callback):
        # Handles individual client connections

class FileTransferClient:
    def send_file(self, file_path, password, progress_callback=None):
        # Encrypts and sends file to server
```

**Protocol Design:**
1. Metadata transmission (JSON header)
2. Encrypted file content transmission
3. Progress callbacks for UI updates
4. Automatic cleanup of temporary files

### SFTP Client Module (`src/core/sftp_client.py`)

Provides SFTP protocol support using paramiko.

```python
class SFTPClient:
    def connect(self):
        # Establishes SFTP connection
        
    def upload_file(self, local_path, remote_path, progress_callback=None):
        # Uploads file via SFTP
        
    def download_file(self, remote_path, local_path, progress_callback=None):
        # Downloads file via SFTP
```

**Features:**
- Password and key-based authentication
- Progress monitoring
- Error handling and recovery
- Connection management

### Authentication Module (`src/core/authentication.py`)

Manages user sessions and authentication.

```python
class AuthenticationManager:
    def login(self, username, password):
        # Authenticates user and creates session
        
    def logout(self):
        # Ends current session
        
    def get_current_user(self):
        # Returns currently authenticated user
```

**Security Features:**
- bcrypt password hashing
- Session management
- Audit logging of authentication events
- Role-based access control

## Database Schema

The application uses SQLAlchemy ORM with the following models:

### User Model
```python
class User(Base):
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.USER)
    created_at = Column(DateTime, default=datetime.utcnow)
```

### AuditLog Model
```python
class AuditLog(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(100), nullable=False)
    details = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)
```

### TransferHistory Model
```python
class TransferHistory(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    file_name = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=False)
    checksum = Column(String(255), nullable=False)
    source = Column(String(255), nullable=False)
    destination = Column(String(255), nullable=False)
    status = Column(String(50), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
```

## Security Implementation

### Encryption Details

**Algorithm**: AES-256 in GCM mode
- **Key Size**: 256 bits (32 bytes)
- **IV Size**: 96 bits (12 bytes) - GCM recommended
- **Tag Size**: 128 bits (16 bytes) - for authentication
- **Salt Size**: 128 bits (16 bytes) - for key derivation

**Key Derivation**: PBKDF2-HMAC-SHA256
- **Iterations**: 100,000 (configurable)
- **Salt**: Random 16-byte salt per encryption
- **Output**: 256-bit encryption key

### File Format (Encrypted Files)

```
[Salt: 16 bytes][IV: 12 bytes][Encrypted Data: Variable][Auth Tag: 16 bytes]
```

### Password Security

- **Hashing**: bcrypt with automatic salt generation
- **Storage**: Only hashed passwords stored in database
- **Validation**: Constant-time comparison to prevent timing attacks

### Network Security

- **Socket Transfer**: Custom protocol with AES-256 encryption
- **SFTP Transfer**: SSH protocol with server authentication
- **No Plain Text**: Passwords never transmitted in plain text

## API Reference

### Configuration API

```python
from src.utils.config import config

# Get database configuration
db_config = config.get_db_config()

# Get logging configuration
log_config = config.get_logging_config()

# Get encryption parameters
enc_config = config.get_encryption_config()
```

### User Management API

```python
from src.database.user_manager import user_manager

# Create new user
user = user_manager.create_user(username, password, email, role)

# Authenticate user
user = user_manager.authenticate_user(username, password)

# Retrieve user
user = user_manager.get_user_by_username(username)
user = user_manager.get_user_by_id(user_id)
```

### Encryption API

```python
from src.core.encryption import encryption_manager

# Encrypt file
encrypted_path = encryption_manager.encrypt_file(file_path, password)

# Decrypt file
decrypted_path = encryption_manager.decrypt_file(encrypted_path, password)
```

### Audit Logging API

```python
from src.database.audit_logger import audit_logger

# Log event
audit_logger.log_event(action, user_id, details)
```

## Development Setup

### Prerequisites

- Python 3.8+
- Git
- Virtual environment (recommended)

### Setup Steps

1. **Clone Repository**
   ```bash
   git clone <repository-url>
   cd encrypted_file_transfer
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database**
   ```bash
   python src/database/models.py
   ```

5. **Run Application**
   ```bash
   python src/main.py
   ```

### Development Tools

**Recommended IDE**: VS Code, PyCharm
**Code Formatting**: black, autopep8
**Linting**: pylint, flake8
**Type Checking**: mypy

### Environment Variables

```bash
# Optional: Override default paths
EFTAPP_CONFIG_PATH=/path/to/config
EFTAPP_DB_PATH=/path/to/database.db
EFTAPP_LOG_PATH=/path/to/logs
```

## Testing

### Running Tests

```bash
# Run all tests
python tests/run_tests.py

# Run specific test file
python -m unittest tests.test_encryption

# Run with verbose output
python tests/run_tests.py -v
```

### Test Structure

- **Unit Tests**: Test individual components in isolation
- **Integration Tests**: Test component interactions
- **GUI Tests**: Test user interface components
- **Security Tests**: Test encryption and authentication

### Writing Tests

```python
import unittest
from src.core.encryption import encryption_manager

class TestEncryption(unittest.TestCase):
    def setUp(self):
        # Test setup code
        
    def test_encrypt_decrypt(self):
        # Test implementation
        
    def tearDown(self):
        # Cleanup code
```

## Extending the Application

### Adding New Transfer Protocols

1. **Create Protocol Module**
   ```python
   # src/core/new_protocol.py
   class NewProtocolClient:
       def send_file(self, file_path, destination, progress_callback=None):
           # Implementation
   ```

2. **Update Main Window**
   ```python
   # Add UI controls in src/gui/main_window.py
   # Add transfer method in start_transfer()
   ```

3. **Update Configuration**
   ```json
   // Add protocol settings to config/settings.json
   ```

### Adding New Encryption Algorithms

1. **Extend Encryption Manager**
   ```python
   # src/core/encryption.py
   def encrypt_file_with_algorithm(self, file_path, password, algorithm):
       # Implementation for new algorithm
   ```

2. **Update Configuration**
   ```json
   // Add algorithm parameters to config/encryption_config.json
   ```

### Adding New Authentication Methods

1. **Extend Authentication Manager**
   ```python
   # src/core/authentication.py
   def authenticate_with_token(self, token):
       # Token-based authentication
   ```

2. **Update User Model**
   ```python
   # Add new fields to src/database/models.py
   ```

### Custom GUI Components

1. **Create Widget Module**
   ```python
   # src/gui/custom_widget.py
   from PyQt5.QtWidgets import QWidget
   
   class CustomWidget(QWidget):
       def __init__(self, parent=None):
           super().__init__(parent)
           # Widget implementation
   ```

2. **Integrate with Main Window**
   ```python
   # Import and use in src/gui/main_window.py
   ```

## Deployment

### Production Deployment

1. **Environment Setup**
   ```bash
   # Create production environment
   python -m venv prod_env
   source prod_env/bin/activate
   pip install -r requirements.txt
   ```

2. **Configuration**
   ```json
   // Update config/settings.json for production
   {
       "database": {
           "type": "postgresql",  // For production use
           "host": "db.example.com",
           "port": 5432,
           "name": "eftapp_prod"
       },
       "logging": {
           "level": "WARNING",
           "file": "/var/log/eftapp/app.log"
       }
   }
   ```

3. **Security Considerations**
   - Use strong database passwords
   - Enable firewall protection
   - Set up SSL/TLS certificates
   - Regular security updates
   - Backup encryption keys securely

### Docker Deployment

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY src/ ./src/
COPY config/ ./config/

EXPOSE 9999
CMD ["python", "src/main.py"]
```

### Database Migration

```python
# For production database changes
from sqlalchemy import create_engine
from src.database.models import Base

def migrate_database():
    engine = create_engine(production_db_url)
    Base.metadata.create_all(engine)
```

### Monitoring and Maintenance

1. **Log Monitoring**
   - Monitor application logs for errors
   - Set up log rotation
   - Configure alerts for critical events

2. **Performance Monitoring**
   - Monitor file transfer speeds
   - Track database performance
   - Monitor memory usage

3. **Security Monitoring**
   - Review audit logs regularly
   - Monitor failed login attempts
   - Check for unusual activity patterns

### Backup Strategy

1. **Database Backup**
   ```bash
   # SQLite backup
   cp config/database.db backup/database_$(date +%Y%m%d).db
   
   # PostgreSQL backup
   pg_dump eftapp_prod > backup/database_$(date +%Y%m%d).sql
   ```

2. **Configuration Backup**
   ```bash
   tar -czf backup/config_$(date +%Y%m%d).tar.gz config/
   ```

3. **Log Archival**
   ```bash
   gzip logs/app.log.$(date +%Y%m%d)
   mv logs/app.log.$(date +%Y%m%d).gz archive/
   ```

---

This developer guide provides the foundation for understanding, maintaining, and extending the Encrypted File Transfer Application. For specific implementation questions, refer to the inline code documentation and comments. 