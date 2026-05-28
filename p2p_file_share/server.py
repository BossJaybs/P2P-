import socket
import threading
import json
import os
from .file_manager import FileManager


class P2PServer:
    """P2P server that listens for incoming file transfers."""

    def __init__(self, port: int = 5555, file_manager: FileManager = None):
        """Initialize P2P server."""
        self.port = port
        self.file_manager = file_manager or FileManager()
        self.server_socket = None
        self.is_running = False
        self.callback = None  # Callback for GUI updates
    
    def set_callback(self, callback):
        """Set callback function for status updates."""
        self.callback = callback
    
    def _emit(self, message: str):
        """Emit callback message."""
        if self.callback:
            self.callback(message)
    
    def start(self):
        """Start the server."""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)
            self.is_running = True
            self._emit(f"Server started on port {self.port}")
            
            # Accept connections in a separate thread
            accept_thread = threading.Thread(target=self._accept_connections, daemon=True)
            accept_thread.start()
        except Exception as e:
            self._emit(f"Error starting server: {str(e)}")
            self.is_running = False
    
    def _accept_connections(self):
        """Accept incoming connections."""
        while self.is_running:
            try:
                client_socket, (client_ip, client_port) = self.server_socket.accept()
                self._emit(f"Connection from {client_ip}:{client_port}")
                
                # Handle client in separate thread
                handler_thread = threading.Thread(
                    target=self._handle_client,
                    args=(client_socket, client_ip, client_port),
                    daemon=True
                )
                handler_thread.start()
            except Exception as e:
                if self.is_running:
                    self._emit(f"Error accepting connection: {str(e)}")
    
    def _handle_client(self, client_socket: socket.socket, client_ip: str, client_port: int):
        """Handle individual client connection."""
        try:
            # Receive metadata (determine action)
            metadata_json = self._recv_all(client_socket, 1024)
            if not metadata_json:
                return

            metadata = json.loads(metadata_json.decode('utf-8'))
            action = metadata.get('action', 'SEND')

            if action == 'LIST':
                # Return list of shared files
                files = self.file_manager.list_shared_files()
                response = json.dumps({'files': files}).encode('utf-8')
                response_padded = response + b' ' * (1024 - len(response))
                client_socket.send(response_padded[:1024])
                return

            if action == 'GET':
                filename = metadata.get('filename')
                if not filename:
                    client_socket.send(json.dumps({'error': 'no filename'}).encode('utf-8') + b' ' * 900)
                    return

                filepath = self.file_manager.get_shared_filepath(filename)
                if not os.path.exists(filepath):
                    err = json.dumps({'error': 'file not found'}).encode('utf-8')
                    client_socket.send(err + b' ' * (1024 - len(err)))
                    return

                filesize = os.path.getsize(filepath)
                # Send metadata to requester
                meta = json.dumps({'filename': filename, 'filesize': filesize}).encode('utf-8')
                meta_padded = meta + b' ' * (1024 - len(meta))
                client_socket.send(meta_padded[:1024])

                # Send file bytes
                with open(filepath, 'rb') as f:
                    while True:
                        chunk = f.read(4096)
                        if not chunk:
                            break
                        client_socket.sendall(chunk)

                # Signal completion
                try:
                    client_socket.send(b'COMPLETE')
                except:
                    pass
                return

            # Default: handle incoming SEND (peer sending file to this server)
            filename = metadata['filename']
            filesize = metadata['filesize']

            self._emit(f"Receiving '{filename}' ({filesize} bytes) from {client_ip}")

            # Get safe filepath
            filepath = self.file_manager.get_safe_filepath(filename)

            # Receive file
            received = 0
            with open(filepath, 'wb') as f:
                while received < filesize:
                    chunk_size = min(4096, filesize - received)
                    chunk = client_socket.recv(chunk_size)
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

                    # Send progress
                    progress = int((received / filesize) * 100)
                    try:
                        client_socket.send(f"{progress}".encode('utf-8'))
                    except:
                        pass

            if received == filesize:
                self._emit(f"File '{filename}' received successfully")
                try:
                    client_socket.send(b"COMPLETE")
                except:
                    pass
            else:
                self._emit(f"Error: Incomplete transfer for '{filename}'")
                try:
                    os.remove(filepath)
                except:
                    pass
                try:
                    client_socket.send(b"ERROR")
                except:
                    pass
        
        except Exception as e:
            self._emit(f"Error handling client: {str(e)}")
        finally:
            client_socket.close()
    
    def _recv_all(self, sock: socket.socket, n: int) -> bytes:
        """Receive exactly n bytes from socket."""
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
    
    def stop(self):
        """Stop the server."""
        self.is_running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except:
                pass
        self._emit("Server stopped")
