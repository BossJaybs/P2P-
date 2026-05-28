import sys
from p2p_file_share.client import P2PClient

def main():
    if len(sys.argv) < 3:
        print("Usage: python list_cli.py <peer_ip> <peer_port>")
        return
    ip = sys.argv[1]
    port = int(sys.argv[2])
    c = P2PClient()
    files = c.list_files(ip, port)
    if not files:
        print("No files reported by peer or request failed.")
        return
    for f in files:
        print(f)

if __name__ == "__main__":
    main()
