# Encrypted File Transfer Application

A secure file transfer application built in Python: **AES-256 encryption** over both a
custom socket protocol and **SFTP**, with a **PyQt5** desktop GUI.

## Features

- **Encrypted transfer** — file contents protected with AES-256 during transmission
- **Two protocols** — custom socket-based transfer and standard SFTP (Paramiko)
- **User authentication** — registration and login with securely hashed passwords
- **Audit logging** — file-transfer and security events written to `logs/`
- **Transfer history** — user accounts and transfer records stored in SQLite
- **Desktop GUI** — PyQt5 interface with login, file browser, and per-transfer progress

## Project Structure

    src/
    ├── core/        # encryption, transfer logic, SFTP client, authentication
    ├── gui/         # main window, login dialog, progress view, file browser
    ├── database/    # models, user management, audit logger
    ├── utils/       # config, logging, helpers
    └── main.py      # entry point
    config/          # settings + encryption config
    tests/
    docs/

## Getting Started

**Prerequisites:** Python 3.8+ (dependencies in `requirements.txt`)

    git clone https://github.com/devesh-bhayani/Encrypted-File-Transfer-Application.git
    cd Encrypted-File-Transfer-Application
    pip install -r requirements.txt
    python src/main.py

On first run, register a user account, then log in to send or receive files.

## Security Notes

- File contents are encrypted with AES-256 before transmission
- Passwords are stored only as salted hashes, never in plaintext
- All transfer and authentication events are audit-logged
