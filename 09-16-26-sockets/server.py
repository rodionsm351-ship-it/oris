import socket
import threading
import protocol

HOST = '127.0.0.1'
PORT = 65432

clients = {}
clients_lock = threading.Lock()

def broadcast(message: str, sender_sock=None):
    payload = message.encode('utf-8')
    with clients_lock:
        for client_sock in list(clients.keys()):
            if client_sock != sender_sock:
                try:
                    protocol.send_message(client_sock, "TEXT", payload)
                except protocol.ProtocolError:
                    pass

def handle_client(conn, addr):
    print(f"Новое подключение: {addr}")
    username = f"User_{addr[1]}"
    
    try:
        while True:
            try:
                message = protocol.recv_message(conn)
                if message is None:
                    print(f"Клиент {username} ({addr}) закрыл соединение.")
                    break
                    
                command, payload = message
                
                if command == "JOIN":
                    username = payload.decode('utf-8')
                    with clients_lock:
                        clients[conn] = username
                    print(f"Клиент {addr} зарегистрировался '{username}'")
                    broadcast(f"В чат зашел {username}!", conn)
                    
                elif command == "TEXT":
                    text = payload.decode('utf-8')
                    formatted_msg = f"[{username}]: {text}"
                    print(f"MSG: {formatted_msg}")
                    broadcast(formatted_msg, conn)
                    
                elif command == "LIST":
                    with clients_lock:
                        user_list = ", ".join(clients.values())
                    response = f"Активные пользователи: {user_list}".encode('utf-8')
                    protocol.send_message(conn, "TEXT", response)
                    
                elif command == "QUIT":
                    print(f"{username} прислал QUIT.")
                    break
                    
                else:
                    error_msg = f"Неизвестная команда: {command}".encode('utf-8')
                    protocol.send_message(conn, "ERR ", error_msg)
                    
            except (ConnectionResetError, BrokenPipeError):
                print(f"Связь с {username} ({addr}) аварийно прервана.")
                break
            except protocol.ProtocolError as e:
                print(f"Ошибка протокола у {username}: {e}")
                break
                
    finally:
        with clients_lock:
            if conn in clients:
                del clients[conn]
        broadcast(f"Пользователь {username} покинул чат.")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Чат-сервер запущен на {HOST}:{PORT}...")
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            thread.start()
    except KeyboardInterrupt:
        print("\n Остановка сервера")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()


