#!/usr/bin/env python3
"""
Encrypted File Transfer Application

A secure file transfer application with AES encryption and support for both
socket-based and SFTP protocols.

Usage:
    python src/main.py
"""

import sys
import os
import traceback
from PyQt5.QtWidgets import QApplication, QMessageBox

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.gui.main_window import MainWindow
from src.database.models import create_db
from src.database.user_manager import user_manager, UserRole
from src.utils.logger import logger
from src.utils.config import config

def setup_application():
    """
    Sets up the application by initializing the database and creating
    a default admin user if none exists.
    """
    try:
        # Create database tables if they don't exist
        create_db()
        logger.info("Database initialized successfully")
        
        # Create default admin user if none exists
        if not user_manager.get_user_by_username('admin'):
            admin_user = user_manager.create_user(
                username='admin',
                password='admin123',  # Default password - should be changed
                email='admin@example.com',
                role=UserRole.ADMIN
            )
            if admin_user:
                logger.info("Default admin user created (username: admin, password: admin123)")
                print("Default admin user created:")
                print("Username: admin")
                print("Password: admin123")
                print("Please change this password after first login!")
            else:
                logger.error("Failed to create default admin user")
        
        return True
        
    except Exception as e:
        logger.error(f"Failed to setup application: {e}")
        logger.error(traceback.format_exc())
        return False

def main():
    """
    Main application entry point.
    """
    try:
        # Create QApplication instance
        app = QApplication(sys.argv)
        app.setApplicationName("Encrypted File Transfer")
        app.setApplicationVersion("1.0.0")
        app.setOrganizationName("SecureTransfer")
        
        logger.info("Starting Encrypted File Transfer Application")
        
        # Setup application (database, default users, etc.)
        if not setup_application():
            QMessageBox.critical(None, "Setup Error", 
                               "Failed to initialize the application. Check the logs for details.")
            return 1
        
        # Create and show main window
        main_window = MainWindow()
        
        # Show login dialog first
        if main_window.show_login():
            main_window.show()
            logger.info("Application started successfully")
            
            # Start the application event loop
            exit_code = app.exec_()
            logger.info(f"Application exited with code: {exit_code}")
            return exit_code
        else:
            logger.info("User cancelled login, exiting application")
            return 0
            
    except Exception as e:
        logger.error(f"Unhandled exception in main: {e}")
        logger.error(traceback.format_exc())
        
        # Show error dialog if possible
        try:
            QMessageBox.critical(None, "Critical Error", 
                               f"An unexpected error occurred:\n{str(e)}\n\n"
                               "Please check the logs for more details.")
        except:
            pass
            
        return 1

if __name__ == '__main__':
    sys.exit(main())
