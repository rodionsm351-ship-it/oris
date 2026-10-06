import struct
import socket


MAX_MESSAGE_SIZE = 1024 * 1024

def recv_exact(sock, size):
    data = b''

    while len(data) < size:
        chunk = sock.recv(size - len(data))
        if not chunk:
            raise ConnectionError("Соединение было закрыто до получения всех данных")

        data += chunk
    return data

def send_message(sock, command: str, payload: bytes):
    command_bytes = command.encode('utf-8')
    command_length = len(command_bytes)

    if command_length > MAX_MESSAGE_SIZE:
        raise ValueError("Команда длинная")
    if len(payload) > MAX_MESSAGE_SIZE:
        raise ValueError("Payload длинный")

    sock.sendall(struct.pack("!I", command_length))
    sock.sendall(command_bytes)
    sock.sendall(struct.pack("!I", len(payload)))
    sock.sendall(payload)


def recv_message(sock):
    command_length_bytes = recv_exact(sock, 4)
    command_length = struct.unpack("!I", command_length_bytes)[0]

    command_bytes = recv_exact(sock, command_length)
    command = command_bytes.decode('utf-8')

    payload_length_bytes = recv_exact(sock, 4)
    payload_length = struct.unpack("!I", payload_length_bytes)[0]

    payload = recv_exact(sock, payload_length)

    return command, payload