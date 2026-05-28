import sys
from p2p_file_share.client import P2PClient

def main():
    if len(sys.argv) < 4:
        print("Usage: python request_cli.py <peer_ip> <peer_port> <filename>")
        return
    ip = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]
    c = P2PClient()
    c.request_file(ip, port, filename)
    print(f"Requested '{filename}' from {ip}:{port}")

if __name__ == "__main__":
    main()
