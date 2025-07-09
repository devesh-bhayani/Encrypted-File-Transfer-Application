import sys
import time
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QApplication
from PyQt5.QtCore import QTimer, pyqtSignal

class TransferProgressWidget(QWidget):
    """
    A widget to display file transfer progress.
    """
    # Signal emitted when cancel button is clicked
    cancel_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start_time = None
        self.last_update_time = None
        self.last_bytes_transferred = 0
        self.setup_ui()
        
    def setup_ui(self):
        """Sets up the user interface."""
        layout = QVBoxLayout(self)
        
        # File name label
        self.file_label = QLabel("No file selected")
        layout.addWidget(self.file_label)
        
        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)
        
        # Status information layout
        status_layout = QHBoxLayout()
        
        # Bytes transferred label
        self.bytes_label = QLabel("0 / 0 bytes")
        status_layout.addWidget(self.bytes_label)
        
        # Transfer speed label
        self.speed_label = QLabel("Speed: 0 KB/s")
        status_layout.addWidget(self.speed_label)
        
        # Estimated time remaining label
        self.eta_label = QLabel("ETA: --:--")
        status_layout.addWidget(self.eta_label)
        
        layout.addLayout(status_layout)
        
        # Cancel button
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.cancel_requested.emit)
        layout.addWidget(self.cancel_button)
        
    def start_transfer(self, file_name, total_size):
        """
        Starts tracking a file transfer.
        
        :param file_name: The name of the file being transferred.
        :param total_size: The total size of the file in bytes.
        """
        self.file_label.setText(f"Transferring: {file_name}")
        self.total_size = total_size
        self.start_time = time.time()
        self.last_update_time = self.start_time
        self.last_bytes_transferred = 0
        self.progress_bar.setValue(0)
        self.update_display(0)
        
    def update_progress(self, file_name, bytes_transferred, total_size):
        """
        Updates the progress display.
        
        :param file_name: The name of the file being transferred.
        :param bytes_transferred: The number of bytes transferred so far.
        :param total_size: The total size of the file in bytes.
        """
        if self.start_time is None:
            self.start_transfer(file_name, total_size)
            
        self.update_display(bytes_transferred)
        
    def update_display(self, bytes_transferred):
        """Updates the display with current progress information."""
        if self.total_size == 0:
            return
            
        # Update progress bar
        progress_percent = int((bytes_transferred / self.total_size) * 100)
        self.progress_bar.setValue(progress_percent)
        
        # Update bytes label
        self.bytes_label.setText(f"{self.format_bytes(bytes_transferred)} / {self.format_bytes(self.total_size)}")
        
        # Calculate and update speed
        current_time = time.time()
        if self.last_update_time and current_time > self.last_update_time:
            time_diff = current_time - self.last_update_time
            bytes_diff = bytes_transferred - self.last_bytes_transferred
            speed = bytes_diff / time_diff  # bytes per second
            self.speed_label.setText(f"Speed: {self.format_bytes(speed)}/s")
            
            # Calculate ETA
            if speed > 0:
                remaining_bytes = self.total_size - bytes_transferred
                eta_seconds = remaining_bytes / speed
                self.eta_label.setText(f"ETA: {self.format_time(eta_seconds)}")
            else:
                self.eta_label.setText("ETA: --:--")
        
        self.last_update_time = current_time
        self.last_bytes_transferred = bytes_transferred
        
    def format_bytes(self, bytes_value):
        """Formats bytes into a human-readable string."""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_value < 1024.0:
                return f"{bytes_value:.1f} {unit}"
            bytes_value /= 1024.0
        return f"{bytes_value:.1f} TB"
        
    def format_time(self, seconds):
        """Formats seconds into a human-readable time string."""
        if seconds < 60:
            return f"{int(seconds)}s"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            seconds = int(seconds % 60)
            return f"{minutes}:{seconds:02d}"
        else:
            hours = int(seconds // 3600)
            minutes = int((seconds % 3600) // 60)
            return f"{hours}:{minutes:02d}:00"
            
    def transfer_complete(self):
        """Marks the transfer as complete."""
        self.progress_bar.setValue(100)
        self.speed_label.setText("Speed: Complete")
        self.eta_label.setText("ETA: Complete")
        self.cancel_button.setText("Close")

if __name__ == '__main__':
    # This is for testing the TransferProgressWidget
    app = QApplication(sys.argv)
    
    widget = TransferProgressWidget()
    widget.setWindowTitle("Transfer Progress Test")
    widget.resize(400, 150)
    widget.show()
    
    # Simulate a file transfer for testing
    def simulate_transfer():
        widget.start_transfer("test_file.txt", 1000000)  # 1MB file
        
        # Simulate progress updates
        timer = QTimer()
        bytes_transferred = 0
        
        def update():
            nonlocal bytes_transferred
            bytes_transferred += 50000  # 50KB increments
            widget.update_progress("test_file.txt", bytes_transferred, 1000000)
            
            if bytes_transferred >= 1000000:
                widget.transfer_complete()
                timer.stop()
        
        timer.timeout.connect(update)
        timer.start(100)  # Update every 100ms
    
    # Start simulation after a short delay
    QTimer.singleShot(1000, simulate_transfer)
    
    sys.exit(app.exec_())
