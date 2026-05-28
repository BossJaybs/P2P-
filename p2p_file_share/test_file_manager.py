#!/usr/bin/env python3
"""
Unit tests for FileManager class to verify collision handling.
Run with: python test_file_manager.py
"""

import unittest
import tempfile
import os
from pathlib import Path
from file_manager import FileManager


class TestFileManager(unittest.TestCase):
    """Test cases for FileManager."""

    def setUp(self):
        """Create temporary directory for testing."""
        self.test_dir = tempfile.mkdtemp()
        self.file_manager = FileManager(download_dir=self.test_dir)
    
    def tearDown(self):
        """Clean up test files."""
        import shutil
        shutil.rmtree(self.test_dir, ignore_errors=True)
    
    def test_directory_creation(self):
        """Test that download directory is created."""
        self.assertTrue(os.path.exists(self.test_dir))
    
    def test_no_collision(self):
        """Test getting path when file doesn't exist."""
        filepath = self.file_manager.get_safe_filepath("test.txt")
        self.assertEqual(os.path.basename(filepath), "test.txt")
    
    def test_collision_handling(self):
        """Test file renaming when collision occurs."""
        # Create initial file
        initial_path = self.file_manager.get_safe_filepath("test.txt")
        Path(initial_path).touch()
        
        # Get path for second file with same name
        collision_path = self.file_manager.get_safe_filepath("test.txt")
        
        # Should be different
        self.assertNotEqual(initial_path, collision_path)
        
        # Should contain timestamp and counter
        basename = os.path.basename(collision_path)
        self.assertIn("test_", basename)
        self.assertIn("_1.txt", basename)
    
    def test_multiple_collisions(self):
        """Test handling of multiple collisions."""
        paths = []
        
        # Create 3 files with same name
        for i in range(3):
            path = self.file_manager.get_safe_filepath("document.pdf")
            paths.append(path)
            Path(path).touch()
        
        # All paths should be unique
        self.assertEqual(len(paths), len(set(paths)))
    
    def test_file_size(self):
        """Test getting file size."""
        filepath = os.path.join(self.test_dir, "test.txt")
        with open(filepath, 'w') as f:
            f.write("Hello World")  # 11 bytes
        
        size = self.file_manager.get_file_size(filepath)
        self.assertEqual(size, 11)
    
    def test_file_exists(self):
        """Test file existence check."""
        # Create a file
        filepath = os.path.join(self.test_dir, "exists.txt")
        Path(filepath).touch()
        
        self.assertTrue(self.file_manager.file_exists("exists.txt"))
        self.assertFalse(self.file_manager.file_exists("nonexistent.txt"))
    
    def test_list_files(self):
        """Test listing files in directory."""
        # Create some files
        Path(os.path.join(self.test_dir, "file1.txt")).touch()
        Path(os.path.join(self.test_dir, "file2.pdf")).touch()
        
        files = self.file_manager.list_files()
        self.assertEqual(len(files), 2)
        self.assertIn("file1.txt", files)
        self.assertIn("file2.pdf", files)


if __name__ == "__main__":
    unittest.main()
