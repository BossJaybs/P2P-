from p2p_file_share.server import P2PServer
import time
import sys

def main():
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5555
    s = P2PServer(port=port)
    s.start()
    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        s.stop()

if __name__ == "__main__":
    main()
