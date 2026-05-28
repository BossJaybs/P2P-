import socket
import json
import os
import threading
from .file_manager import FileManager


class P2PClient:
    """P2P client for sending files to peers."""

    def __init__(self):
        """Initialize P2P client."""
        self.callback = None
    
    def set_callback(self, callback):
        """Set callback function for status updates."""
        self.callback = callback
    
    def _emit(self, message: str):
        """Emit callback message."""
        if self.callback:
            self.callback(message)
    
    def send_file(self, peer_ip: str, peer_port: int, filepath: str):
        """
        Send file to peer.
        Runs in a separate thread to avoid blocking UI.
        """
        thread = threading.Thread(
            target=self._send_file_thread,
            args=(peer_ip, peer_port, filepath),
            daemon=True
        )
        thread.start()
    
    def _send_file_thread(self, peer_ip: str, peer_port: int, filepath: str):
        """Internal method to send file in separate thread."""
        try:
            # Validate file exists
            if not os.path.exists(filepath):
                self._emit(f"Error: File not found: {filepath}")
                return
            
            # Get file size
            filesize = os.path.getsize(filepath)
            filename = os.path.basename(filepath)
            
            # Connect to peer
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_ip, peer_port))
            self._emit(f"Connected to {peer_ip}:{peer_port}")
            
            # Send metadata
            metadata = {
                'filename': filename,
                'filesize': filesize
            }
            metadata_json = json.dumps(metadata).encode('utf-8')
            
            # Pad metadata to 1024 bytes
            metadata_padded = metadata_json + b' ' * (1024 - len(metadata_json))
            sock.send(metadata_padded[:1024])
            
            self._emit(f"Sending '{filename}' ({filesize} bytes)")
            
            # Send file
            sent = 0
            with open(filepath, 'rb') as f:
                while sent < filesize:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    sock.sendall(chunk)
                    sent += len(chunk)
                    
                    # Receive progress acknowledgment
                    try:
                        ack = sock.recv(1024).decode('utf-8')
                        if ack and ack.isdigit():
                            progress = int(ack)
                            self._emit(f"Sending '{filename}': {progress}%")
                    except:
                        pass
            
            # Wait for completion signal
            response = sock.recv(1024).decode('utf-8')
            if response == "COMPLETE":
                self._emit(f"File '{filename}' sent successfully")
            else:
                self._emit(f"Error: Transfer failed for '{filename}'")
            
            sock.close()
        
        except socket.timeout:
            self._emit(f"Error: Connection timeout to {peer_ip}:{peer_port}")
        except ConnectionRefusedError:
            self._emit(f"Error: Connection refused by {peer_ip}:{peer_port}")
        except Exception as e:
            self._emit(f"Error sending file: {str(e)}")

    def list_files(self, peer_ip: str, peer_port: int) -> list:
        """Request list of shared files from a peer."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_ip, peer_port))
            # Send LIST action
            metadata = json.dumps({'action': 'LIST'}).encode('utf-8')
            metadata_padded = metadata + b' ' * (1024 - len(metadata))
            sock.send(metadata_padded[:1024])

            resp = self._recv_all(sock, 1024)
            sock.close()
            if not resp:
                return []
            data = json.loads(resp.decode('utf-8').strip() or '{}')
            return data.get('files', [])
        except Exception as e:
            self._emit(f"Error requesting file list: {str(e)}")
            return []

    def request_file(self, peer_ip: str, peer_port: int, filename: str):
        """Request a single file from peer and save it to downloads."""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((peer_ip, peer_port))
            metadata = json.dumps({'action': 'GET', 'filename': filename}).encode('utf-8')
            metadata_padded = metadata + b' ' * (1024 - len(metadata))
            sock.send(metadata_padded[:1024])

            # Receive metadata about the file
            meta = self._recv_all(sock, 1024)
            if not meta:
                self._emit("No response from peer")
                sock.close()
                return

            info = json.loads(meta.decode('utf-8').strip() or '{}')
            if 'error' in info:
                self._emit(f"Peer error: {info.get('error')}")
                sock.close()
                return

            filename = info['filename']
            filesize = info['filesize']
            self._emit(f"Receiving '{filename}' ({filesize} bytes) from {peer_ip}")

            # Save to download dir
            # If FileManager methods available, use it; else save in cwd
            try:
                fm = FileManager()
                savepath = fm.get_safe_filepath(filename)
            except Exception:
                savepath = filename

            received = 0
            with open(savepath, 'wb') as f:
                while received < filesize:
                    chunk = sock.recv(min(4096, filesize - received))
                    if not chunk:
                        break
                    f.write(chunk)
                    received += len(chunk)

            if received == filesize:
                self._emit(f"File '{filename}' received successfully")
            else:
                self._emit(f"Error: Incomplete transfer for '{filename}'")

            sock.close()
        except Exception as e:
            self._emit(f"Error requesting file: {str(e)}")
