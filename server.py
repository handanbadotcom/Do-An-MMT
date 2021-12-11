import socket
import threading
import pandas
import requests
from bs4 import *
from datetime import date

FORMAT = 'utf8' 
HEADER = 64 #chiều dài gói tin
PORT = 5080
SERVER = '127.0.0.1' #socket.gethostbyname(socket.gethostname())
ADDRESS=(SERVER,PORT)
DISSMSG = "break"
#khởi tạo socket
server=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind(ADDRESS)

#gọi hàm này khi có client kết nối
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
    #nếu client crash thì code nhảy vào except
    except:         
        print("client crashed")   
        conn.close()

    conn.close()    
    return

#khơỉ động server
def start():
    server.listen()
    print("[LISTEN]", SERVER)
    while True: 
        conn, addr = server.accept() 
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print("[ACTIVE CONNECTION]", {threading.active_count()})

def readData():
    data = pandas.read_json('Data.json') #đọc vào file json
    find= 'USD' #tên ngoại tệ
    f =data[data['Ngoai te'].str.contains(find)] # xuất ra thông tin ngoại tệ

def crawlData(url):
    #tao ket noi va tao soup
    r = requests.get(url).content
    soup = BeautifulSoup(r,'lxml')

    #chon bang can trich du lieu
    allTables = soup.find_all('table',class_='jrPage')
    table = allTables[1]

    #lay data can thiet
    rawData=[]
    for td in table.find_all('td'):
        if td.text!='' and td.text!=' ':
            rawData.append(td.text)

    Data=[]
    for data in rawData:
        a = data.replace(data[0]+data[1],data[1])
        Data.append(a)

    #tach data thanh cac truong du lieu khac nhau
    #ten truong
    Title=[]
    #so thu tu
    STT=[]
    #ma ngoai te (USD,EUR,...)
    NT=[]
    #ten ngoai te
    Ten_NT=[]
    Mua=[]
    Ban=[]
    index=1

    for i in range(1,6):
        Title.append(Data[index])
        index += 1
    #đổi lại tên cột thành ko dấu đễ dễ thực hiện
    Title[0] = 'STT'
    Title[1] = 'Ngoai te'
    Title[2] = 'Ten ngoai te'
    Title[3] = 'Mua'
    Title[4] = 'Ban'

    for i in range(1,8):
        STT.append(Data[index])
        index += 1
        NT.append(Data[index])
        index += 1
        Ten_NT.append(Data[index])
        index += 1
        Mua.append(Data[index])
        index += 1
        Ban.append(Data[index])
        index += 1

    #chuyen thanh data frame
    Struct = {Title[0]:pandas.Series(STT),
            Title[1]:pandas.Series(NT),
    #       Title[2]:pandas.Series(Ten_NT), #có dấu bị lỗi
            Title[3]:pandas.Series(Mua),
            Title[4]:pandas.Series(Ban),}


    DF = pandas.DataFrame(Struct)
    return DF
    
print("[STARTING]")
#print(SERVER)
#start()

