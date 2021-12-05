import socket

FORMAT = 'utf8'
HEADER = 64
PORT = 5080
SERVER = '127.0.0.1' #thay đổi địa chỉ theo địa chỉ của server
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS) 

def send_msg(msg):
    client.sendall(msg.encode(FORMAT))

#muốn gửi gì cho server thì sử dụng hàm send_msg
#vd nhắn tin cho server cho đến khi thoát bằng break
message = ""
while message!='break':
    message=input()
    send_msg(message)
    print(client.recv(HEADER).decode(FORMAT))

    





