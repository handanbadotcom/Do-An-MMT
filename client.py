import socket

from server import ADDRESS

FORMAT = 'utf-8'
HEADER = 64
PORT = 5070
SERVER = "127.0.0.1"
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
