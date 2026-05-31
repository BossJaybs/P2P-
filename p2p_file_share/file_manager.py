import os
from datetime import datetime
from pathlib import Path


class FileManager:
    """Handles file operations and collision avoidance."""

    def __init__(self, download_dir: str = None):
        """Initialize FileManager with a download directory."""
        if download_dir is None:
            download_dir = os.path.join(os.path.expanduser("~"), "P2P_Downloads")
        
        # Directory where incoming files are saved
        self.download_dir = download_dir
        # Directory for files you want to share with peers
        self.shared_dir = os.path.join(os.path.expanduser("~"), "P2P_Shared")
        self._ensure_download_dir()
        self._ensure_shared_dir()
    
    def _ensure_download_dir(self):
        """Create download directory if it doesn't exist."""
        os.makedirs(self.download_dir, exist_ok=True)
    
    def get_safe_filepath(self, filename: str) -> str:
        """
        Get a safe filepath, auto-renaming if file exists.
        Uses timestamp + counter format: filename_20240528_120000_1.ext
        """
        filepath = os.path.join(self.download_dir, filename)
        
        # If file doesn't exist, return as-is
        if not os.path.exists(filepath):
            return filepath
        
        # File exists, generate new name with timestamp and counter
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        counter = 1
        
        while True:
            new_filename = f"{name}_{timestamp}_{counter}{ext}"
            new_filepath = os.path.join(self.download_dir, new_filename)
            if not os.path.exists(new_filepath):
                return new_filepath
            counter += 1
    
    def get_file_size(self, filepath: str) -> int:
        """Get file size in bytes."""
        return os.path.getsize(filepath)
    
    def file_exists(self, filename: str) -> bool:
        """Check if file exists in download directory."""
        filepath = os.path.join(self.download_dir, filename)
        return os.path.exists(filepath)
    
    def list_files(self) -> list:
        """List all files in download directory."""
        if not os.path.exists(self.download_dir):
            return []
        return os.listdir(self.download_dir)

    def _ensure_shared_dir(self):
        """Create shared directory if it doesn't exist."""
        os.makedirs(self.shared_dir, exist_ok=True)

    def list_shared_files(self) -> list:
        """Return list of files available for remote browsing.

        The remote browser should show both explicitly shared files and files
        that were previously received into the download directory so peers can
        discover content that has already landed on the machine.
        """
        files = []
        seen = set()

        for directory in (self.shared_dir, self.download_dir):
            if not os.path.exists(directory):
                continue

            for filename in os.listdir(directory):
                filepath = os.path.join(directory, filename)
                if not os.path.isfile(filepath):
                    continue

                if filename in seen:
                    continue

                seen.add(filename)
                files.append(filename)

        return sorted(files)

    def get_shared_filepath(self, filename: str) -> str:
        """Resolve shared file path (no auto-renaming)."""
        return os.path.join(self.shared_dir, filename)
