import socket
import json
import pandas

FORMAT = 'utf8'
HEADER = 2048
PORT = 5090
SERVER = '127.0.0.1' #thay đổi địa chỉ theo địa chỉ của server
ADDRESS = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDRESS) 

def send_msg(msg):
    client.sendall(msg.encode(FORMAT))

def searchCurrency( data, currency): #hàm tra cứu
   f=data[data['Ngoai te'].str.contains(currency)] # tìm trong dataframe cột 'Ngoai te' có chuỗi nào chứa chuỗi con currency ko
   return(f)
    

#muốn gửi gì cho server thì sử dụng hàm send_msg
#vd nhắn tin cho server cho đến khi thoát bằng break hoặc yêu cầu data bằng cách gõ request data
message = ""
while message!='break':
    message=input()
    send_msg(message)
    if message == 'request data':
     data = client.recv(HEADER).decode(FORMAT) #client nhận string 
     output = pandas.read_json(data) #load string vừa nhận được thành dataframe
     currency=searchCurrency(output,'USD')
     print(currency)
    print(client.recv(HEADER).decode(FORMAT))

    





