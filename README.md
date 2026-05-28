# P2P File Share

A simple peer-to-peer file sharing application with a desktop GUI built using Python's Tkinter library.

## Features

- **P2P File Transfer**: Send files directly between peers over the network
- **Desktop GUI**: User-friendly Tkinter interface for easy file selection and transfer
- **Auto-Rename**: Automatically handles file name collisions with timestamp-based renaming
- **Real-time Progress**: Display transfer progress percentage during file operations
- **Multi-threaded**: Handle concurrent file transfers without blocking the UI
- **Manual Peer Discovery**: Connect to peers by manually entering their IP address and port
- **Activity Logging**: View detailed logs of all transfers and connection events

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## Installation

1. Clone or download the P2P File Share project
2. Navigate to the `p2p_file_share` directory
3. Run the application:

```bash
python main.py
```

Or run it from the repository root:

```bash
python p2p_file_share/main.py
```

## Usage

### Starting the Application

If you are already inside the `p2p_file_share` directory:

```bash
python main.py
```

If you are at the repository root:

```bash
python p2p_file_share/main.py
```

The application window will open with the P2P File Share GUI.

### Sending a File

1. Click the **Send File** tab
2. Click **Browse** to select the file you want to send
3. Enter the peer's **IP address** (e.g., 192.168.1.100)
4. Enter the peer's **port** (default: 5555)
5. Click **Send File** to initiate the transfer

### Receiving a File

The application automatically listens for incoming files on port 5555. When a peer sends you a file:

1. The file is automatically received and saved
2. If a file with the same name exists, it's renamed with a timestamp (e.g., `document_20240528_120000_1.pdf`)
3. Check the **Status & Logs** tab to see transfer activity
4. Go to **Settings** tab and click **Open Directory** to view received files

### Finding Your IP Address

To share your IP with others:

1. Go to the **Settings** tab
2. You'll see your **Local IP Address** and **Listening Port**
3. Share this information with peers who want to send you files

## Project Structure

```
p2p_file_share/
├── main.py              # Entry point for the application
├── gui.py               # Tkinter GUI implementation
├── server.py            # P2P server for receiving files
├── client.py            # P2P client for sending files
├── file_manager.py      # File operations and collision handling
└── README.md            # This file
```

## How It Works

### Architecture

1. **Server Component**: Multi-threaded TCP server listening on port 5555
   - Accepts incoming connections from peers
   - Receives file metadata (filename, size)
   - Receives file data in chunks
   - Sends progress updates back to sender

2. **Client Component**: Connects to remote peers
   - Sends file metadata as JSON
   - Transfers file in 4KB chunks
   - Receives progress acknowledgments
   - Handles timeout and connection errors

3. **File Manager**: Handles file operations
   - Checks for file name collisions
   - Creates safe file paths with timestamp-based renaming
   - Manages the download directory

4. **GUI**: Tkinter-based interface with 3 tabs
   - **Send File**: File selection and peer connection
   - **Status & Logs**: Activity log and transfer history
   - **Settings**: Server info, download directory, and app status

### Protocol

The application uses a simple JSON-based protocol:

1. **Metadata Exchange** (1024 bytes):
   ```json
   {
     "filename": "document.pdf",
     "filesize": 1048576
   }
   ```

2. **File Transfer**: Raw binary data in 4KB chunks

3. **Progress Acknowledgment**: Percentage string (0-100)

4. **Completion Signal**: "COMPLETE" or "ERROR"

## Configuration

### Port

The default listening port is **5555**. You can modify this in `server.py`:

```python
self.server = P2PServer(port=5555, file_manager=self.file_manager)
```

### Download Directory

By default, received files are saved to `~/P2P_Downloads`. You can change this in the GUI by modifying the `FileManager` initialization in `gui.py`:

```python
self.file_manager = FileManager(download_dir="/custom/path")
```

## Security Notes

⚠️ **Important**: This is a simple file sharing application for local networks. Consider the following:

1. **No Authentication**: Anyone who knows your IP and port can send you files
2. **No Encryption**: Files are transferred in plain text over the network
3. **No Verification**: No checksum verification for file integrity

For production use with sensitive data, consider:
- Running on a private network only
- Implementing TLS/SSL encryption
- Adding authentication tokens
- Adding file integrity checks (MD5/SHA256)

## Troubleshooting

### "Connection Refused" Error

- Ensure the peer's IP address and port are correct
- Check that the peer's firewall allows incoming connections on port 5555
- Verify both computers are on the same network

### File Not Found Error

- Ensure the selected file still exists before sending
- Check file permissions on your system

### Transfer Hangs

- Check your network connection
- Try sending a smaller file first
- Look for firewall or antivirus software blocking the connection

## License

This project is provided as-is for educational and personal use.

## Future Enhancements

Possible improvements for future versions:

- Multiple file selection and batch transfers
- Resume interrupted transfers
- File encryption with optional passwords
- Drag-and-drop file selection
- Automatic local network peer discovery (mDNS/Bonjour)
- Transfer history with retry options
- File compression before transfer
- Bandwidth throttling options
