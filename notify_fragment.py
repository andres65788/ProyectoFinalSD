import socket

def notify_fragment_available(fragment_name):
    msg = f"PUB:fragmentos:{fragment_name}"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 14000))
        sock.sendall(msg.encode())

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Uso: python notify_fragment.py <fragmento.bin>")
        exit(1)
    notify_fragment_available(sys.argv[1])