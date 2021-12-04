import socket

FORMAT = 'utf8'
HEADER = 64
PORT = 5080
SERVER = '127.0.0.1' #thay đổi địa chỉ theo địa chỉ của server
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS) 

def send_msg(msg):
    '''
    message= msg.encode(FORMAT)
    msg_length= len(message)
    send_length= str(msg_length).encode(FORMAT)
    send_length=  b' '*(HEADER-len(send_length))
    client.send(send_length)
    client.send(message)
    '''
    client.sendall(msg.encode(FORMAT))

send_msg("alo")
input()
send_msg("break")    

