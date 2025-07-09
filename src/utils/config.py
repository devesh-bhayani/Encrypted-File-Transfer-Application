import json
import os

class Config:
    """
    Handles loading and accessing configuration settings from JSON files.
    """
    def __init__(self, settings_path='config/settings.json', encryption_path='config/encryption_config.json'):
        self.settings = self._load_json(settings_path)
        self.encryption = self._load_json(encryption_path)
        self._adjust_paths()

    def _load_json(self, path):
        """Loads a JSON file from the given path."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            raise Exception(f"Configuration file not found at: {path}")
        except json.JSONDecodeError:
            raise Exception(f"Error decoding JSON from file: {path}")

    def _adjust_paths(self):
        """
        Adjusts file paths in the config to be relative to the project root.
        This assumes the script is run from the project root.
        """
        if 'database' in self.settings and 'path' in self.settings['database']:
            self.settings['database']['path'] = os.path.join(self.get_project_root(), self.settings['database']['path'])
        
        if 'logging' in self.settings and 'file' in self.settings['logging']:
            self.settings['logging']['file'] = os.path.join(self.get_project_root(), self.settings['logging']['file'])

    def get_project_root(self):
        """
        Returns the absolute path to the project root directory.
        This assumes the 'src' directory is in the project root.
        """
        return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

    def get_db_config(self):
        """Returns the database configuration."""
        return self.settings.get('database', {})

    def get_logging_config(self):
        """Returns the logging configuration."""
        return self.settings.get('logging', {})

    def get_encryption_config(self):
        """Returns the encryption configuration."""
        return self.encryption

# Create a single instance of the Config class to be used throughout the application
config = Config()
