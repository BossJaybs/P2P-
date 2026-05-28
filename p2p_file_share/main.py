#!/usr/bin/env python3
"""
P2P File Share - A simple peer-to-peer file sharing application
with a Tkinter desktop GUI.

Run this file to start the application:
    python main.py
"""

import tkinter as tk
try:
    # When run as module: python -m p2p_file_share.main
    from .gui import P2PFileShareGUI
except Exception:
    # When run as script from inside package folder: python main.py
    from gui import P2PFileShareGUI


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    
    # Create GUI
    app = P2PFileShareGUI(root)
    
    # Handle window closing
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    
    # Start GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()
