import socket
import threading

PORT = 5050 
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS=(SERVER,PORT)

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(connection, address):
    pass

def start():
    server.listen()
    while True:
        connection, address = server.accept()
        thread = threading.Thread(target=handle_client, args=(connection, address))
        thread.start()
        print({threading.activeCount()})


print(SERVER)
start()
