# Quick Start Guide - P2P File Share

Get started with P2P File Share in 5 minutes!

## Installation

### Step 1: Verify Python Installation

Make sure you have Python 3.6 or higher installed:

```bash
python --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### Step 2: No Dependencies Required!

This project uses **only Python's standard library** - no external packages to install. You can run it immediately!

## Running the Application

### Step 1: Navigate to the Project Directory

```bash
cd p2p_file_share
```

### Step 2: Start the Application

```bash
python main.py
```

The P2P File Share window will open with a user-friendly interface.

## Basic Usage

### Setup (First Time)

1. When the app starts, the server automatically begins listening on port 5555
2. Go to the **Settings** tab to find your **Local IP Address**
3. Share this IP with your peers so they can send you files

### Sending a File

1. Click the **Send File** tab
2. Click **Browse** to select a file from your computer
3. Enter the recipient's **IP address** (ask them to check Settings tab)
4. Enter the **port** (default is 5555)
5. Click **Send File**
6. Check the **Status & Logs** tab to monitor transfer progress

### Receiving a File

1. Files are automatically received and saved to your **P2P_Downloads** folder
2. If a file with the same name already exists, it's automatically renamed
3. You can view received files by clicking **Open Directory** in the Settings tab

## Example Workflow

**Computer A (Sender):**
1. Open P2P File Share
2. Click Send File → Browse → Select "vacation.zip"
3. Enter Computer B's IP: `192.168.1.100`
4. Port: `5555`
5. Click Send File

**Computer B (Receiver):**
1. App is running and listening
2. File automatically arrives and is saved
3. Can find it in Settings → Open Directory

## Tips

- **Finding IP Addresses**: Both computers must be on the same network. Check Settings tab for your Local IP.
- **Firewall**: If transfer fails, check your firewall settings. Port 5555 must be allowed.
- **Large Files**: Works with any file size. Progress updates show percentage completion.
- **Multiple Transfers**: Can send to multiple peers or receive while sending.

## Troubleshooting

### "Connection Refused"
- Verify the peer's IP address is correct
- Ensure the receiving computer is running the app
- Check firewall settings allow port 5555

### "File Not Found"
- Ensure the file hasn't been moved or deleted since selection
- Try again with a different file

### GUI Won't Open
- Make sure Tkinter is installed (usually included with Python)
- On Linux, you might need: `sudo apt-get install python3-tk`

## File Organization

```
p2p_file_share/
├── main.py                    ← Run this file to start
├── gui.py                     ← Tkinter interface
├── server.py                  ← Receives files
├── client.py                  ← Sends files
├── file_manager.py            ← Handles file operations
├── test_file_manager.py       ← Tests (optional)
├── requirements.txt           ← Dependencies (none needed!)
├── README.md                  ← Full documentation
└── QUICKSTART.md              ← This file
```

## Next Steps

- Read the full [README.md](README.md) for advanced features and configuration
- Check [Advanced Usage](#advanced-usage) section below

## Advanced Usage

### Custom Download Directory

Edit `gui.py` and change line 22:

```python
self.file_manager = FileManager(download_dir="/path/to/custom/directory")
```

### Custom Port

Edit `gui.py` and change line 24:

```python
self.server = P2PServer(port=8080, file_manager=self.file_manager)
```

Then update the port in the Send File tab to match.

### Run Tests

Verify file collision handling:

```bash
python test_file_manager.py
```

## System Requirements

- **Windows**: Python 3.6+ with Tkinter
- **macOS**: Python 3.6+ (includes Tkinter)
- **Linux**: Python 3.6+ with `python3-tk` package

On Linux, install Tkinter if needed:
```bash
sudo apt-get install python3-tk
```

---

Enjoy simple P2P file sharing! 🚀
