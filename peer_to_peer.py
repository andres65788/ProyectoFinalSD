import socket
import threading
import sys
import time
import os

def handle_peer(conn, addr):
    try:
        print(f"[+] Conectado desde {addr}")
        requested_fragment = conn.recv(1024).decode().strip()
        file_path = f"fragments/{requested_fragment}"
        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                data = f.read()
                conn.sendall(data)
                print(f"[✓] Fragmento '{requested_fragment}' enviado a {addr}")
        else:
            conn.sendall(b"[X] Fragmento no encontrado")
    except Exception as e:
        print(f"[!] Error con {addr}: {e}")
    finally:
        conn.close()

def peer_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', port))
    server.listen(5)
    print(f"[SERVIDOR] Nodo escuchando en puerto {port}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_peer, args=(conn, addr))
        thread.start()

def request_fragment(peer, fragment_name):
    host, port = peer
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
            sock.sendall(fragment_name.encode())
            with open(f"fragments/{fragment_name}", 'wb') as f:
                while True:
                    data = sock.recv(1024)
                    if not data: break
                    f.write(data)
            print(f"[✓] Fragmento '{fragment_name}' recibido desde {host}:{port}")
    except Exception as e:
        print(f"[X] Error al solicitar fragmento: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python peer_to_peer.py <mi_puerto> <peer1_host:port> [<peer2_host:port> ...]")
        sys.exit(1)

    my_port = int(sys.argv[1])
    peers = [tuple(p.split(":")) for p in sys.argv[2:]]
    peers = [(h, int(p)) for h, p in peers if int(p) != my_port]

    threading.Thread(target=peer_server, args=(my_port,), daemon=True).start()
    time.sleep(1)

    while True:
        fragment = input("Fragmento a solicitar (o 'exit'): ")
        if fragment.lower() == 'exit':
            break
        for peer in peers:
            request_fragment(peer, fragment)