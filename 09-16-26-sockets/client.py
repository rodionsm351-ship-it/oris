import socket
import threading
import sys
import protocol

HOST = '127.0.0.1'
PORT = 65432

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

    try:
        protocol.send_message(sock, "JOIN", username.encode('utf-8'))
    except Exception as e:
        print(f"Ошибка отправки JOIN: {e}")
        sock.close()
        return

    receive_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
    receive_thread.start()

    print("Вы подключились к чату! Доступные команды: /list, /quit")
    
    try:
        while True:
            text = input("")
            
            if not receive_thread.is_alive():
                break

            if text == "/quit":
                protocol.send_message(sock, "QUIT", b"")
                break
            elif text == "/list":
                protocol.send_message(sock, "LIST", b"")
            elif text:
                protocol.send_message(sock, "TEXT", text.encode('utf-8'))
                
    except KeyboardInterrupt:
        print("\nВыход из чата...")
    except (ConnectionResetError, BrokenPipeError):
        print("\n[!] Соединение разорвано.")
    finally:
        sock.close()

if __name__ == "__main__":
    start_client()
