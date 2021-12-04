import socket

FORMAT = 'utf-8'
HEADER = 64
PORT = 5080
SERVER = '127.0.0.1' #thay đổi địa chỉ theo địa chỉ của server
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS)
