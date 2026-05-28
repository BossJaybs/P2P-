# P2P File Share - Usage Examples

Real-world scenarios and how to use P2P File Share.

## Example 1: Sharing Documents Between Offices

**Scenario**: You need to send a large presentation file to a colleague in a different office, both on the same company network.

**Step 1: Get Your IP Address**
1. Open P2P File Share on your computer
2. Go to Settings tab
3. Note your Local IP Address (e.g., `192.168.1.50`)
4. Tell your colleague: "My IP is 192.168.1.50"

**Step 2: Colleague Prepares to Receive**
1. They open P2P File Share on their computer
2. They see the Settings tab shows their own IP
3. Their computer is now listening for incoming files

**Step 3: Send the File**
1. Click "Send File" tab
2. Click "Browse" → select "Q1_Presentation.pptx"
3. Enter colleague's IP: `192.168.1.65`
4. Port: `5555`
5. Click "Send File"
6. Watch progress in "Status & Logs" tab

**Result**: Colleague's P2P File Share automatically receives and saves the file to ~/P2P_Downloads/Q1_Presentation.pptx

---

## Example 2: Receiving Multiple Files

**Scenario**: Your team is sharing photos from a company event. Multiple people send you files.

**What Happens Automatically**:
1. First person sends "event_photos.zip"
   - Saved as: `~/P2P_Downloads/event_photos.zip`

2. Second person also sends "event_photos.zip"
   - Auto-renamed to: `~/P2P_Downloads/event_photos_20240528_143000_1.zip`

3. Third person sends "event_photos.zip"
   - Auto-renamed to: `~/P2P_Downloads/event_photos_20240528_143005_2.zip`

**No manual intervention needed** - no files are overwritten!

---

## Example 3: Local Backup to Network Drive

**Scenario**: You want to send important files to a backup PC on your home network.

**Setup**:
- Backup PC: Runs P2P File Share, IP = `192.168.1.100`
- Your PC: Sends files to backup

**Process**:
```
Your PC                          Backup PC
┌──────────────┐                ┌─────────────┐
│ Main Computer│ ──send──────> │ Backup Drive│
│  (Sender)    │    files      │  (Receiver) │
└──────────────┘                └─────────────┘
   192.168.1.50                   192.168.1.100
```

1. Send your documents to 192.168.1.100:5555
2. Files automatically saved to backup location
3. Can be repeated daily for incremental backups

---

## Example 4: Quick File Transfer at Meetings

**Scenario**: You're at a meeting and need to share documents with 3 people.

**Quick Setup** (takes 2 minutes):
1. Open P2P File Share on your laptop
2. Share your IP: "Send files to 192.168.1.75"
3. Each person opens P2P File Share on their device
4. Each person's computer is now listening

**Transfer Process**:
1. Select your meeting agenda document
2. Enter attendee 1 IP: 192.168.1.80 → Send
3. Enter attendee 2 IP: 192.168.1.85 → Send
4. Enter attendee 3 IP: 192.168.1.90 → Send

All three receive the document within seconds, no email needed!

---

## Example 5: Batch File Transfer

**Scenario**: Need to send 5 related files to a single peer.

**Method 1: One at a Time**
1. Select file 1 → Send
2. Wait for completion
3. Select file 2 → Send
4. Repeat...

**Method 2: Compress First** (Recommended)
1. Create a ZIP file with all 5 files: `project_files.zip`
2. Send the ZIP: Single transfer, faster
3. Recipient extracts the ZIP

**Result**: All files transferred efficiently

---

## Example 6: Large Video File Transfer

**Scenario**: You have a 2GB video file to send to a video editor on your network.

**Step 1: Prepare**
1. Ensure stable network connection
2. Don't use bandwidth-heavy activities
3. Keep both computers powered on

**Step 2: Send**
1. Click "Send File" tab
2. Browse → select your `2GB_video.mp4`
3. Enter video editor's IP: `192.168.1.200`
4. Click "Send File"

**Step 3: Monitor Progress**
- View "Status & Logs" tab
- Watch percentage increase: 5% → 25% → 50% → 100%
- Transfer takes 5-15 minutes depending on network speed

**Step 4: Verify**
- Video editor receives file automatically
- File saved with proper name
- Ready to open and edit

---

## Example 7: Cross-Platform Transfer

**Scenario**: Share files between Windows, macOS, and Linux computers on the same network.

P2P File Share works on all platforms identically:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│ Windows PC  │       │  macOS Mac  │       │ Linux Box   │
│ 192.168.1.50│◄─────►│ 192.168.1.51│◄─────►│ 192.168.1.52│
└─────────────┘       └─────────────┘       └─────────────┘
All running P2P File Share
```

- Windows user can send to macOS user
- macOS user can send to Linux
- Linux user can send back to Windows
- No compatibility issues!

---

## Example 8: Handling Interrupted Transfer

**Scenario**: Transfer was interrupted by network issue or closed window.

**What Happens**:
1. Transfer stops (partially received file might be deleted)
2. No corrupted files left behind
3. Simply retry the transfer

**Retry Steps**:
1. The original file is still on sender's computer
2. Send File tab → Browse → select file again
3. Enter peer IP again
4. Click "Send File" again
5. Transfer restarts from beginning

No manual cleanup needed!

---

## Example 9: Text Files and Documents

**Scenario**: Sharing small text files, PDFs, or documents.

**Typical Files**:
- PDFs (reports, invoices)
- Documents (Word, Excel, text files)
- Configuration files
- Source code files

**Performance**: Instant transfer (usually under 1 second)

**Example**:
```
Send report.pdf (2.3 MB) to colleague
→ Clicks Send File
→ 100% complete in 3 seconds
→ Colleague sees notification and can open
```

---

## Example 10: Troubleshooting Failed Transfer

**Scenario**: "Connection Refused" error appears.

**Checklist**:
1. ✓ Is the recipient's computer running P2P File Share?
   - Ask them to check if app is open

2. ✓ Is the IP address correct?
   - Ask them to verify IP in Settings tab
   - Check for typos (e.g., 192.168.1.50 not 192.168.1.5)

3. ✓ Are you on the same network?
   - Both computers should be on same WiFi or wired network
   - Can you ping them? `ping 192.168.1.100`

4. ✓ Is port 5555 open?
   - Check firewall settings
   - May need to whitelist P2P File Share app

5. ✓ Try again
   - Network glitches happen
   - Simply retry the transfer

---

## Technical Details for Advanced Users

### Memory Usage
- Server: ~10MB base + per-connection overhead
- Client: Minimal, scales with file size
- Streaming design: doesn't load entire file into RAM

### Network Usage
- No compression by default (data sent as-is)
- 4KB chunks for balanced throughput
- ACK messages: <100 bytes per chunk

### Disk Usage
- Files saved to `~/P2P_Downloads`
- Auto-rename prevents data loss
- No temporary files left behind

### CPU Usage
- Multi-threaded design minimizes blocking
- No encoding/decoding overhead
- Minimal computational cost

---

## Security Notes for These Examples

⚠️ For **trusted networks only** (home, office):
- No encryption in transit
- No password protection
- No integrity verification

**Recommendations**:
1. Use only on private networks
2. Don't send sensitive credentials
3. Verify peer identity before sending
4. For sensitive data, use VPN + P2P File Share

---

That's it! These examples cover most real-world use cases. For more information, see [README.md](README.md).
