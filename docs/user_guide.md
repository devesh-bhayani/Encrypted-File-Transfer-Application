# Encrypted File Transfer Application - User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Getting Started](#getting-started)
4. [Using the Application](#using-the-application)
5. [File Transfer Methods](#file-transfer-methods)
6. [Security Features](#security-features)
7. [Troubleshooting](#troubleshooting)
8. [FAQ](#faq)

## Introduction

The Encrypted File Transfer Application is a secure, user-friendly solution for transferring files with end-to-end encryption. It supports both custom socket-based transfers and standard SFTP protocols, ensuring your files remain protected during transmission.

### Key Features
- **AES-256 Encryption**: Military-grade encryption for all file transfers
- **Multiple Transfer Methods**: Socket-based and SFTP protocols
- **User Authentication**: Secure login system with role-based access
- **Real-time Progress**: Live transfer progress monitoring
- **Audit Logging**: Comprehensive activity tracking
- **Cross-platform**: Works on Windows, macOS, and Linux

## Installation

### Prerequisites
- Python 3.8 or higher
- 50MB of free disk space
- Network connectivity for file transfers

### Installation Steps

1. **Download the Application**
   ```bash
   # Clone or download the application files
   git clone https://your-repository-url.git
   cd encrypted_file_transfer
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the Application**
   ```bash
   python src/main.py
   ```

   On first run, the application will:
   - Create the database
   - Set up default configuration
   - Create a default admin user

## Getting Started

### First Launch

1. **Start the Application**
   ```bash
   python src/main.py
   ```

2. **Login with Default Credentials**
   - Username: `admin`
   - Password: `admin123`
   
   **Important**: Change this password immediately after first login!

3. **Create Your User Account**
   - Click "Register" to create a new user account
   - Use a strong password (minimum 8 characters)
   - Provide a valid email address

### Main Interface Overview

The application window consists of several key areas:

- **File Browser** (Left Panel): Navigate and select files to transfer
- **Transfer Controls** (Right Panel): Configure transfer settings
- **Progress Monitor**: Real-time transfer progress display
- **Activity Log**: Shows all application activities and events

## Using the Application

### Selecting Files for Transfer

1. **Navigate the File Browser**
   - Use the left panel to browse your local file system
   - Click on folders to expand them
   - Single-click on a file to select it

2. **File Selection**
   - Only one file can be selected at a time
   - The selected file path will be highlighted
   - Ensure you have read permissions for the selected file

### Socket-Based File Transfer

Socket-based transfer uses the application's custom encrypted protocol.

#### Sending Files

1. **Configure Connection**
   - Enter the recipient's IP address in the "Host" field
   - Set the port number (default: 9999)
   - Ensure the recipient is running the server

2. **Select and Send**
   - Choose a file in the file browser
   - Click "Send File"
   - Enter an encryption password when prompted
   - Monitor progress in the progress widget

#### Receiving Files

1. **Start the Server**
   - Click "Start Server" button
   - The server will listen on the specified port
   - Files will be saved to the `downloads` folder

2. **Share Connection Details**
   - Provide your IP address and port to the sender
   - Ensure your firewall allows incoming connections

3. **Decrypting Received Files**
   - After a file is received (e.g., `document.txt.enc`), you will need to decrypt it.
   - Go to the "File Utilities" section.
   - Click "Decrypt File".
   - Select the encrypted file you received.
   - Enter the password that the sender used to encrypt the file.
   - Choose a location to save the decrypted file.

### SFTP File Transfer

SFTP transfer uses the standard SSH File Transfer Protocol.

#### Configuration

1. **Enter Server Details**
   - Host: SFTP server address
   - Port: SFTP port (default: 22)
   - Username: Your SFTP username
   - Password: Your SFTP password

2. **Set Remote Path**
   - Enter the destination path on the remote server
   - Use forward slashes (/) for path separators
   - Ensure you have write permissions to the destination

#### Transferring Files

1. **Select File**
   - Choose a file using the file browser
   - Verify the file size and type

2. **Initiate Transfer**
   - Click "Send File via SFTP"
   - The application will connect and transfer the file
   - Monitor progress in the progress widget

## File Transfer Methods

### Socket Transfer vs. SFTP

| Feature | Socket Transfer | SFTP Transfer |
|---------|----------------|---------------|
| Encryption | AES-256 (Custom) | SSH Protocol |
| Setup | Simple | Requires SFTP server |
| Firewall | May need configuration | Standard port (22) |
| Authentication | Password-based | Username/password or keys |
| Resume Support | No | Yes (server dependent) |

### Choosing the Right Method

- **Use Socket Transfer** for:
  - Direct peer-to-peer transfers
  - Maximum security with custom encryption
  - Simple setup without server requirements

- **Use SFTP Transfer** for:
  - Transfers to established servers
  - Integration with existing infrastructure
  - Standard protocol compliance

## Security Features

### Encryption

- **Algorithm**: AES-256 in GCM mode
- **Key Derivation**: PBKDF2 with 100,000 iterations
- **Authentication**: Built-in message authentication
- **Unique Keys**: Each transfer uses a unique encryption key

### Authentication

- **Password Security**: Bcrypt hashing with salt
- **Session Management**: Secure session tokens
- **Role-Based Access**: Admin and user roles
- **Audit Logging**: All activities are logged

### Best Practices

1. **Use Strong Passwords**
   - Minimum 8 characters
   - Include uppercase, lowercase, numbers, and symbols
   - Avoid common words or personal information

2. **Secure Your Environment**
   - Keep the application updated
   - Use secure networks when possible
   - Regularly review audit logs

3. **File Handling**
   - Verify file integrity after transfer
   - Securely delete sensitive files after transfer
   - Use unique passwords for each transfer

## Troubleshooting

### Common Issues

#### Login Problems
- **Issue**: Cannot login with credentials
- **Solution**: 
  - Verify username and password are correct
  - Check if account exists
  - Contact administrator for password reset

#### Connection Failures
- **Issue**: Cannot connect to remote host
- **Solution**:
  - Verify IP address and port
  - Check firewall settings
  - Ensure target service is running

#### Transfer Interruptions
- **Issue**: File transfer stops or fails
- **Solution**:
  - Check network connectivity
  - Verify sufficient disk space
  - Restart the transfer

#### Permission Errors
- **Issue**: Cannot read file or write to destination
- **Solution**:
  - Check file permissions
  - Ensure destination directory exists
  - Run with appropriate user privileges

### Error Messages

| Error | Meaning | Solution |
|-------|---------|----------|
| "File not found" | Selected file doesn't exist | Refresh file browser, select valid file |
| "Connection refused" | Cannot reach remote host | Check address, port, and firewall |
| "Authentication failed" | Invalid credentials | Verify username and password |
| "Permission denied" | Insufficient file access | Check file/directory permissions |

### Getting Help

1. **Check Activity Log**
   - Review the activity log for error details
   - Look for specific error messages

2. **Verify Configuration**
   - Check connection settings
   - Verify file paths and permissions

3. **Contact Support**
   - Provide error messages and logs
   - Include steps to reproduce the issue

## FAQ

### General Questions

**Q: Is the application free to use?**
A: Yes, this is an open-source application available for free use.

**Q: What file types can be transferred?**
A: Any file type can be transferred - documents, images, videos, archives, etc.

**Q: Is there a file size limit?**
A: No hard limit, but very large files may take longer to transfer and require more memory.

**Q: Can I transfer multiple files at once?**
A: Currently, only single file transfers are supported. Transfer files one at a time.

### Security Questions

**Q: How secure is the encryption?**
A: The application uses AES-256 encryption, which is considered military-grade and highly secure.

**Q: Can files be intercepted during transfer?**
A: Files are encrypted before transmission, making interception ineffective without the password.

**Q: Are passwords stored securely?**
A: Yes, passwords are hashed using bcrypt with salt and never stored in plain text.

**Q: What happens to files after transfer?**
A: Original files remain unchanged. Encrypted temporary files are automatically deleted.

### Technical Questions

**Q: What ports does the application use?**
A: Default socket port is 9999 (configurable). SFTP uses port 22 by default.

**Q: Can I use this on a corporate network?**
A: Yes, but check with your IT department about firewall and security policies.

**Q: Does the application work offline?**
A: The application requires network connectivity for file transfers but can run locally for file management.

**Q: How do I backup my user data?**
A: The database file in the `config` directory contains user data and can be backed up.

---

For additional support or questions not covered in this guide, please refer to the developer documentation or contact the application administrators. 