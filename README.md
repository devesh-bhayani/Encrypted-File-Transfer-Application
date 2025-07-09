# Encrypted File Transfer Application

This project is a comprehensive Encrypted File Transfer Application built in Python. It provides a secure and user-friendly way to transfer files using AES encryption and SFTP protocols.

## Features

-   **Secure File Transfer**: Utilizes AES-256 encryption to protect file content during transmission.
-   **Multiple Protocols**: Supports both a custom socket-based transfer protocol and the standard SFTP protocol.
-   **User Authentication**: Robust user registration, login, and session management system with secure password hashing.
-   **Real-time Monitoring**: Live progress bars and status updates for file transfers.
-   **Audit Logging**: Comprehensive logging of all file transfers and security-related events.
-   **Intuitive GUI**: A clean and easy-to-use graphical user interface built with Tkinter/PyQt.
-   **Database Integration**: Uses SQLite/PostgreSQL for user management and transfer history.
-   **Concurrent Transfers**: Supports multiple file transfers simultaneously using threading.
-   **Resume Capability**: Ability to resume interrupted file transfers.

## Project Structure

```
/encrypted_file_transfer/
├── src/
│   ├── core/
│   │   ├── encryption.py
│   │   ├── file_transfer.py
│   │   ├── sftp_client.py
│   │   └── authentication.py
│   ├── gui/
│   │   ├── main_window.py
│   │   ├── login_dialog.py
│   │   ├── transfer_progress.py
│   │   └── file_browser.py
│   ├── database/
│   │   ├── models.py
│   │   ├── user_manager.py
│   │   └── audit_logger.py
│   ├── utils/
│   │   ├── config.py
│   │   ├── logger.py
│   │   └── helpers.py
│   └── main.py
├── config/
│   ├── settings.json
│   ├── encryption_config.json
│   └── database.db
├── tests/
├── docs/
├── requirements.txt
└── README.md
```

## Getting Started

### Prerequisites

-   Python 3.8+
-   See `requirements.txt` for a full list of dependencies.

### Installation

1.  Clone the repository:
    ```bash
    git clone https://example.com/your-repo.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd encrypted_file_transfer
    ```
3.  Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```
4.  Run the application:
    ```bash
    python src/main.py
    ```

## Usage

Detailed usage instructions will be provided in the user documentation.

## Contributing

Contributions are welcome! Please follow the standard fork, branch, and pull request workflow.

## License

This project is licensed under the MIT License - see the LICENSE.md file for details.
