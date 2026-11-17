import socket

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MASSAGE = "DISCONNECT"
SERVER = "0.0.0.0"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(SERVER, PORT)
