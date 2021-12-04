import socket
import threading

FORMAT = 'utf8'
HEADER = 64 #chiều dài gói tin
PORT = 5080
SERVER = '127.0.0.1' #socket.gethostbyname(socket.gethostname())
ADDRESS=(SERVER,PORT)
DISSMSG = "break"
#khởi tạo socket
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDRESS)

def handle_client(conn, addr):
    print("[NEW CONNECTION]", {addr})
    connection = True
    
    try:
        while connection!=False:
            msg= conn.recv(HEADER).decode(FORMAT)
            if msg:
                if msg == DISSMSG: 
                    connection = False
                print(addr,':',msg)
                conn.sendall("received".encode(FORMAT))

    except:         
        print("client crashed")   
        conn.close()

    conn.close()    
    return

def start():
    server.listen()
    print("[LISTEN]", SERVER)
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTION]", {threading.active_count()})


print("[STARTING]")
#print(SERVER)
start()

