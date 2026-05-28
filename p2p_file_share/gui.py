import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import socket
import os
import threading
from .server import P2PServer
from .client import P2PClient
from .file_manager import FileManager


class P2PFileShareGUI:
    """Tkinter GUI for P2P file sharing application."""

    def __init__(self, root):
        """Initialize GUI."""
        self.root = root
        self.root.title("P2P File Share")
        self.root.geometry("700x600")
        
        # Initialize components
        self.file_manager = FileManager()
        self.server = P2PServer(file_manager=self.file_manager)
        self.client = P2PClient()
        
        # Create widgets first so UI elements (like log_text) exist
        self._create_widgets()

        # Set callbacks (safe now that widgets are created)
        self.server.set_callback(self._log_message)
        self.client.set_callback(self._log_message)

        # Start server on init
        self.server.start()
    
    def _create_widgets(self):
        """Create GUI widgets."""
        # Main notebook (tabs)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tab 1: Send File
        send_frame = ttk.Frame(notebook)
        notebook.add(send_frame, text="Send File")
        self._create_send_tab(send_frame)
        
        # Tab 2: Status
        status_frame = ttk.Frame(notebook)
        notebook.add(status_frame, text="Status & Logs")
        self._create_status_tab(status_frame)
        
        # Tab 3: Settings
        settings_frame = ttk.Frame(notebook)
        notebook.add(settings_frame, text="Settings")
        self._create_settings_tab(settings_frame)
    
    def _create_send_tab(self, parent):
        """Create Send File tab."""
        # Title
        title_label = ttk.Label(parent, text="Send File to Peer", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # File selection
        file_frame = ttk.LabelFrame(parent, text="Select File to Send", padding=10)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        browse_button = ttk.Button(file_frame, text="Browse", command=self._browse_file)
        browse_button.pack(side=tk.RIGHT, padx=5)

        # Remote browse button (opens list of shared files on remote peer)
        remote_button = ttk.Button(file_frame, text="Browse Remote", command=self._browse_remote)
        remote_button.pack(side=tk.RIGHT, padx=5)
        
        # Peer connection
        peer_frame = ttk.LabelFrame(parent, text="Peer Connection", padding=10)
        peer_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # IP input
        ttk.Label(peer_frame, text="Peer IP:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.peer_ip_var = tk.StringVar(value="127.0.0.1")
        ip_entry = ttk.Entry(peer_frame, textvariable=self.peer_ip_var, width=30)
        ip_entry.grid(row=0, column=1, sticky=tk.EW, padx=5)
        
        # Port input
        ttk.Label(peer_frame, text="Peer Port:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.peer_port_var = tk.StringVar(value="5555")
        port_entry = ttk.Entry(peer_frame, textvariable=self.peer_port_var, width=30)
        port_entry.grid(row=1, column=1, sticky=tk.EW, padx=5)
        
        peer_frame.columnconfigure(1, weight=1)
        
        # Send button
        send_button = ttk.Button(parent, text="Send File", command=self._send_file)
        send_button.pack(pady=15)
    
    def _create_status_tab(self, parent):
        """Create Status & Logs tab."""
        # Title
        title_label = ttk.Label(parent, text="Activity Log", font=("Arial", 14, "bold"))
        title_label.pack(pady=10)
        
        # Log display
        self.log_text = scrolledtext.ScrolledText(
            parent,
            height=20,
            width=80,
            state=tk.DISABLED,
            bg="#f0f0f0",
            font=("Courier", 9)
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Clear log button
        clear_button = ttk.Button(parent, text="Clear Log", command=self._clear_log)
        clear_button.pack(pady=5)
    
    def _create_settings_tab(self, parent):
        """Create Settings tab."""
        # Server Info
        server_frame = ttk.LabelFrame(parent, text="Server Information", padding=15)
        server_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Get local IP
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
        except:
            local_ip = "127.0.0.1"
        
        ttk.Label(server_frame, text="Local IP Address:").pack(anchor=tk.W, pady=5)
        ttk.Label(server_frame, text=local_ip, font=("Arial", 12, "bold"), foreground="blue").pack(anchor=tk.W, padx=20, pady=2)
        
        ttk.Label(server_frame, text="Listening Port:").pack(anchor=tk.W, pady=5)
        ttk.Label(server_frame, text="5555", font=("Arial", 12, "bold"), foreground="blue").pack(anchor=tk.W, padx=20, pady=2)
        
        # Download directory
        download_frame = ttk.LabelFrame(parent, text="Download Directory", padding=15)
        download_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(download_frame, text="Received files are saved to:").pack(anchor=tk.W, pady=5)
        ttk.Label(
            download_frame,
            text=self.file_manager.download_dir,
            font=("Arial", 10, "bold"),
            foreground="blue",
            wraplength=500
        ).pack(anchor=tk.W, padx=20, pady=2)
        
        open_dir_button = ttk.Button(
            download_frame,
            text="Open Directory",
            command=self._open_download_dir
        )
        open_dir_button.pack(pady=10)
        
        # Status
        status_frame = ttk.LabelFrame(parent, text="Status", padding=15)
        status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        status_label = ttk.Label(
            status_frame,
            text="✓ Server is running",
            font=("Arial", 11),
            foreground="green"
        )
        status_label.pack(anchor=tk.W, pady=5)
    
    def _browse_file(self):
        """Browse for file to send."""
        filepath = filedialog.askopenfilename(
            title="Select file to send",
            initialdir=os.path.expanduser("~")
        )
        if filepath:
            self.selected_file = filepath
            filename = os.path.basename(filepath)
            self.file_label.config(text=filename, foreground="black")
            self._log_message(f"Selected file: {filename}")

    def _browse_remote(self):
        """Open a dialog to list files from the remote peer and allow requesting one."""
        # Create dialog window
        dlg = tk.Toplevel(self.root)
        dlg.title("Remote Files")
        dlg.geometry("500x400")

        # Peer inputs
        frame = ttk.Frame(dlg)
        frame.pack(fill=tk.X, padx=10, pady=8)

        ttk.Label(frame, text="Peer IP:").grid(row=0, column=0, sticky=tk.W)
        ip_var = tk.StringVar(value=self.peer_ip_var.get())
        ip_entry = ttk.Entry(frame, textvariable=ip_var, width=20)
        ip_entry.grid(row=0, column=1, sticky=tk.W, padx=5)

        ttk.Label(frame, text="Port:").grid(row=0, column=2, sticky=tk.W, padx=(10,0))
        port_var = tk.StringVar(value=self.peer_port_var.get())
        port_entry = ttk.Entry(frame, textvariable=port_var, width=8)
        port_entry.grid(row=0, column=3, sticky=tk.W, padx=5)

        fetch_btn = ttk.Button(frame, text="Fetch List", command=lambda: threading.Thread(target=self._fetch_remote_files, args=(ip_var.get(), port_var.get(), listbox, fetch_btn), daemon=True).start())
        fetch_btn.grid(row=0, column=4, sticky=tk.W, padx=10)

        # Files list
        listbox = tk.Listbox(dlg, height=15)
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=8)

        btn_frame = ttk.Frame(dlg)
        btn_frame.pack(fill=tk.X, padx=10, pady=6)

        request_btn = ttk.Button(btn_frame, text="Request Selected", command=lambda: threading.Thread(target=self._request_selected_remote, args=(ip_var.get(), port_var.get(), listbox), daemon=True).start())
        request_btn.pack(side=tk.RIGHT)

        close_btn = ttk.Button(btn_frame, text="Close", command=dlg.destroy)
        close_btn.pack(side=tk.RIGHT, padx=6)

    def _fetch_remote_files(self, ip, port, listbox, button):
        """Fetch file list from peer and populate the listbox."""
        try:
            self._log_message(f"Requesting file list from {ip}:{port}...")
            files = self.client.list_files(ip, int(port))
            def update():
                listbox.delete(0, tk.END)
                for f in files:
                    listbox.insert(tk.END, f)
                button.config(state=tk.NORMAL)
            self.root.after(0, update)
            self._log_message(f"Received {len(files)} files from {ip}")
        except Exception as e:
            self._log_message(f"Failed to fetch list: {e}")
            self.root.after(0, lambda: button.config(state=tk.NORMAL))

    def _request_selected_remote(self, ip, port, listbox):
        """Request the file currently selected in the listbox."""
        try:
            sel = listbox.curselection()
            if not sel:
                self._log_message("No file selected")
                return
            filename = listbox.get(sel[0])
            self._log_message(f"Requesting '{filename}' from {ip}:{port}")
            self.client.request_file(ip, int(port), filename)
        except Exception as e:
            self._log_message(f"Request failed: {e}")
    
    def _send_file(self):
        """Send selected file to peer."""
        if not hasattr(self, 'selected_file') or not self.selected_file:
            messagebox.showerror("Error", "Please select a file first")
            return
        
        try:
            peer_ip = self.peer_ip_var.get().strip()
            peer_port = int(self.peer_port_var.get().strip())
            
            if not peer_ip:
                messagebox.showerror("Error", "Please enter peer IP address")
                return
            
            if peer_port <= 0 or peer_port > 65535:
                messagebox.showerror("Error", "Invalid port number (1-65535)")
                return
            
            self._log_message(f"Initiating transfer to {peer_ip}:{peer_port}")
            self.client.send_file(peer_ip, peer_port, self.selected_file)
        
        except ValueError:
            messagebox.showerror("Error", "Invalid port number")
    
    def _log_message(self, message: str):
        """Add message to log."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _clear_log(self):
        """Clear log display."""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete("1.0", tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _open_download_dir(self):
        """Open download directory in file manager."""
        try:
            import subprocess
            import platform
            
            if platform.system() == "Darwin":  # macOS
                subprocess.Popen(["open", self.file_manager.download_dir])
            elif platform.system() == "Windows":
                os.startfile(self.file_manager.download_dir)
            else:  # Linux
                subprocess.Popen(["xdg-open", self.file_manager.download_dir])
        except Exception as e:
            messagebox.showerror("Error", f"Could not open directory: {str(e)}")
    
    def on_closing(self):
        """Handle window closing."""
        self.server.stop()
        self.root.destroy()
