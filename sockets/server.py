import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "0.0.0.0"
FORMAT = 'utf-8'
DISCONNECT_MASSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((SERVER, PORT))

def handle_client(conn, addr):
    print(f"new connect {addr}")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode(FORMAT)

        if msg == DISCONNECT_MASSAGE:
            connected = False

        print(f"{addr} {msg}")

    conn.close()


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"new active connection {threading.activeCount() - 1}")

print("starting server")
start()


