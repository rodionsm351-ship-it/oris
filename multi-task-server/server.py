import socket
import threading
import protocol

HOST = '0.0.0.0'
PORT = 5555

clients = {}
clients_lock = threading.Lock()

tasks = []
tasks_lock = threading.Lock()


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
                
                if command == "ADD":
                    try:
                        task_text = payload.decode('utf-8').strip()
                        if not task_text:
                            raise ValueError("Пустая задача")
                    except Exception as e:
                        error_msg = f"Ошибка при добавлении задачи: {e}"
                        protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                        continue

                    new_task = {
                        "text": task_text,
                        "done": False
                    }
                    with tasks_lock:
                        tasks.append(new_task)

                    response = "Задача добавлена"
                    protocol.send_message(conn, "TEXT", response.encode('utf-8'))
                    
                elif command == "LIST":
                    with tasks_lock:
                        if not tasks:
                            response = "Нет активных задач."
                        else:
                            lines = []
                            for idx, task in enumerate(tasks, start=1):
                                status = "[x]" if task["done"] else "[ ]"
                                lines.append(f"{idx}. {status} {task['text']}")

                            response = "\n".join(lines)
                    protocol.send_message(conn, "TEXT", response.encode('utf-8'))
                    
                elif command == "DONE":
                    try:
                        task_idx = int(payload.decode('utf-8')) - 1
                    except ValueError:
                        error_msg = "Неверный формат индекса задачи."
                        protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                        continue

                    if task_idx < 0 or task_idx >= len(tasks):
                        error_msg = "Неверный индекс задачи:"
                        protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                        continue

                    with tasks_lock:
                        if task_idx < 0 or task_idx >= len(tasks):
                            error_msg = "Неверный индекс задачи:"
                            protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                            continue
                        else:
                            tasks[task_idx]["done"] = True

                        response = "Задача помечена как выполненная"
                        protocol.send_message(conn, "TEXT", response.encode('utf-8'))

                elif command == "DELETE":
                    try:
                        task_idx = int(payload.decode('utf-8')) - 1
                    except ValueError:
                        error_msg = "Неверный формат индекса задачи."
                        protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                        continue

                    with tasks_lock:
                        if task_idx < 0 or task_idx >= len(tasks):
                            error_msg = "Задача с таким индексом не существует."
                            protocol.send_message(conn, "ERR ", error_msg.encode('utf-8'))
                            continue
                        else:
                            tasks.pop(task_idx)

                    response = "Задача удалена"
                    protocol.send_message(conn, "TEXT", response.encode('utf-8'))
                    
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
        broadcast(f"Пользователь {username} покинул доску задач")
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