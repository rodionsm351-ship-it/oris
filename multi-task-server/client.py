import socket
import threading
import sys
import protocol

HOST = '127.0.0.1'
PORT = 5555

def receive_messages(sock):
    try:
        while True:
            message = protocol.recv_message(sock)
            if message is None:
                print("\n Сервер закрыл соединение.")
                break
                
            command, payload = message
            if command == "TEXT" or command == "ERR ":
                print(f"\n{payload.decode('utf-8')}")
            else:
                print(f"\nНеизвестная команда от сервера: {command}")
                
    except (ConnectionResetError, BrokenPipeError):
        print("\n Аварийный обрыв связи с сервером.")
    except Exception as e:
        print(f"\n Ошибка: {e}")
    finally:
        print("Нажмите Enter для выхода...")
        sock.close()

def start_client():
    username = input("Введите ваше имя: ").strip()
    if not username:
        username = "Guest"

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(" Не удалось подключиться к серверу.")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    receive_thread.start()

    print("Вы подключились к доске задач! Доступные команды: /add, /list, /done, /delete, /quit")
    
    try:
        while True:
            text = input("").strip()
            if not text:
                continue

            parts = text.strip().split(' ', 1)
            cmd = parts[0]
            arg = parts[1] if len(parts) > 1 else ""

            if not receive_thread.is_alive():
                break

            if cmd == "/add":
                if not arg:
                    print("Использование: /add <текст задачи>")
                    continue
                protocol.send_message(sock, "ADD", arg.encode('utf-8'))

            elif cmd == "/list":
                protocol.send_message(sock, "LIST", b"")

            elif cmd == "/done":
                if not arg.isdigit():
                    print("Использование: /done <номер задачи>")
                    continue
                protocol.send_message(sock, "DONE", arg.encode('utf-8'))
            elif cmd == "/delete":
                if not arg.isdigit():
                    print("Использование: /delete <номер задачи>")
                    continue
                protocol.send_message(sock, "DELETE", arg.encode('utf-8'))
            elif cmd == "/quit":
                protocol.send_message(sock, "QUIT", b"")
                break
            else:
                print(f"\nНеизвестная команда: {cmd}")

                
    except KeyboardInterrupt:
        print("\nВыход из чата...")
    except (ConnectionResetError, BrokenPipeError):
        print("\n[!] Соединение разорвано.")
    finally:
        sock.close()


if __name__ == "__main__":
    start_client()