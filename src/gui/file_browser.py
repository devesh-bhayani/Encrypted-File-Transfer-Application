import sys
import os
from PyQt5.QtWidgets import QTreeView, QFileSystemModel, QApplication, QMainWindow
from PyQt5.QtCore import QDir

class FileBrowser(QTreeView):
    """
    A widget to browse the local file system.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.model = QFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        self.setModel(self.model)
        self.setRootIndex(self.model.index(QDir.homePath())) # Start at home directory

        # Customize view
        self.setSortingEnabled(True)
        self.setColumnWidth(0, 250) # Set width for the name column

    def get_selected_file_path(self):
        """
        Returns the path of the currently selected file.
        
        :return: A string with the file path, or None if no file is selected.
        """
        index = self.currentIndex()
        if not index.isValid():
            return None
        return self.model.filePath(index)

if __name__ == '__main__':
    # This is for testing the FileBrowser widget
    app = QApplication(sys.argv)
    
    # Create a main window to host the browser
    main_window = QMainWindow()
    main_window.setWindowTitle("File Browser Test")
    main_window.setGeometry(100, 100, 800, 600)
    
    file_browser = FileBrowser()
    main_window.setCentralWidget(file_browser)
    
    main_window.show()
    sys.exit(app.exec_())
