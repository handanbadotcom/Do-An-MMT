import socket
import threading

FORMAT = 'utf-8'
HEADER = 64
PORT = 5070
SERVER = socket.gethostbyname(socket.gethostname())
ADDRESS=(SERVER,PORT)
DISSMSG = "break"

server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn, addr):
    print("[NEW CONNECTION]", {addr})
    connection = True
    while connection:
        message_length= conn.recv(HEADER).decode(FORMAT)
        message_length = int(message_length)
        message = conn.recv(message_length).decode(FORMAT)
        if message == DISSMSG: 
            connection = False
        print(addr,':',message)

    conn.close()
def start():
    server.listen()
    print("[LISTEN]", SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTION]", {threading.activeCount()})


print("[STARTING]")
#print(SERVER)
start()
