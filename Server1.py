import tkinter as Tk
import socket
import threading
import json
import requests
import pandas 
from datetime import datetime
from bs4 import BeautifulSoup
from datetime import *
import datetime


HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 65432
FORMAT = "utf8"
NUM_OF_DAY = 3 #so ngay toi da cua file json
#link web
url = 'https://sbv.gov.vn/TyGia/faces/TyGiaMobile.jspx?_afrLoop=14339020310096506&_afrWindowMode=0&_adf.ctrl-state=1786p90txj_21'

def initJsonFile(tenFile, NumOfDay):  #Khoi tao file JSON du lieu trong voi so ngay cho truoc
    sotmp = []
    chutmp = []
    STT = [1,2,3,4,5,6,7]
    NT = ['USD', 'EUR', 'JPY', 'GBP', 'CHF', 'AUD', 'CAD']
    TenNT = ['Do la My','Dong Euro','Yen Nhat', 'Bang Anh', 'Pho rang Thuy Si', 'Do la Uc', 'Do la Canada']
    for i in range(0, 7*NumOfDay):
        sotmp.append(0)
        chutmp.append('a')
    Struct = {'Ngày'         : pandas.Series(chutmp),
              'STT'          : pandas.Series(STT * NumOfDay),
              'Ngoại tệ'     : pandas.Series(NT * NumOfDay),
              'Tên Ngoại tệ' : pandas.Series(TenNT * NumOfDay),
              'Mua'          : pandas.Series(sotmp),
              'Bán'          : pandas.Series(sotmp),}
    DF = pandas.DataFrame(Struct)
    with open(tenFile, 'w+') as file:
        DF.to_json(file, orient='index')
def updateFile(fileName, NumOfDay, Ban, Mua):
    with open(fileName) as json_file:
        data = pandas.read_json(json_file, orient='index')
    now = datetime.datetime.now()
    today=now.strftime("%m/%d/%Y")
    if(data.iat[7 * NumOfDay - 1, 0] != today):    #data of new day
        #push up data for new day
        for i in range(0, 7 * (NumOfDay - 1)):
            for j in range(0, 6):
                data.iat[i, j] = data.iat[i + 7, j]
        #replace data of column day
        for i in range(-7, 0):
            data.iat[i, 0] = today
    for i in range(-7, 0):
        data.iat[i,4] = Mua[i]
        data.iat[i,5] = Ban[i]
    #print(data)
    with open(fileName, 'w+') as file:
        data.to_json(file, orient='index')
def updateData(url, fileName, NumOfDay):
    #tao ket noi va tao soup
    r = requests.get(url).content
    soup = BeautifulSoup(r,'lxml')

    #chon bang can trich du lieu
    allTables = soup.find_all('table', class_='jrPage')
    table = allTables[1]

    #lay data can thiet
    rawData = []
    for td in table.find_all('td'):
        if td.text != '' and td.text != ' ':
            rawData.append(td.text)

    Data = []
    for data in rawData:
        a = data.replace(data[0]+data[1], data[1])
        Data.append(a)

    Title = []  #ten truong
    STT = []    #so thu tu  
    NT = []     #ma ngoai te (USD,EUR,...)    
    Ten_NT = [] #ten ngoai te
    Mua = []    #Gia mua
    Ban = []    #Gia ban
    index = 1

    #tach data thanh cac truong du lieu khac nhau
    for i in range(1,6):
        Title.append(Data[index])
        index += 1
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
    #Ghi du lieu da moi vao file
    updateFile(fileName, NumOfDay, Ban, Mua)
class App(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)

        self.title("Server")
        self.geometry("500x500")
        self.resizable(width = False, height = False)

        addressLabel = Tk.Label(self, text = 'Server IP Address: '+ HOST).pack()
        titleLabel = Tk.Label(self, text = 'CLIENT STATUS').pack()
        self.waitingLabel = Tk.Label(self, text = 'Waiting for Client...')
        self.waitingLabel.pack()

        self.conent =Tk.Frame(self)
        self.data = Tk.Listbox(self.conent, height = 20, width = 70)
        self.conent.pack_configure()
        self.scroll = Tk.Scrollbar(self.conent)
        self.scroll.pack(side = 'right', fill= 'both')
        self.data.config(yscrollcommand = self.scroll.set)
        self.scroll.config(command = self.data.yview)
        self.data.pack()

        closeButton = Tk.Button(self, text = 'Close', command=lambda: closeServer()).pack()
        
        def handleClientSignUp(connection, nClient, clientStatus):
            username = connection.recv(1024).decode(FORMAT)
           
            with open('Accounts.json') as accountData:
                accountList = json.load(accountData)
            accountData.close()

            usernameList = []
            for account in accountList['accounts']:
                usernameList.append(account['username'])

            if username in usernameList:
                connection.sendall('False'.encode(FORMAT))
                return
                
            connection.sendall('True'.encode(FORMAT))
            password = connection.recv(1024).decode(FORMAT)

            newAccount = {"username": username, "password": password}
            accountList['accounts'].append(newAccount)

            with open('Accounts.json', 'w') as accountData:
                json.dump(accountList, accountData, indent = 2)
            accountData.close()

            tmp = "Client " + str(nClient) + " has signed up with username: " + username
            clientStatus.append(tmp)

        def handleClientLogin(connection, nClient, onlineClient, clientStatus):
            username = connection.recv(1024).decode(FORMAT)
            connection.sendall(username.encode(FORMAT))
            password = connection.recv(1024).decode(FORMAT)
            
            with open('Accounts.json') as accountData:
                accountList = json.load(accountData)
            accountData.close()

            if username in onlineClient:
                connection.sendall('Exist'.encode(FORMAT))
                return None

            clientAccount = {"username": username, "password": password}

            if clientAccount not in accountList['accounts']:
                connection.sendall('False'.encode(FORMAT))
                return None
            
            connection.sendall('True'.encode(FORMAT))

            onlineClient.append(username)
            tmp = "Client " + str(nClient) + " has logged in as: " + username
            clientStatus.append(tmp)
            return username

        def handleClient(self, connection, address, nClient, onlineClient, clientStatus):
            self.waitingLabel['text'] = ''
            tmp = "Connected by Client " + str(nClient) + ": " +  str(address)
            clientStatus.append(tmp)
            usingAccount = None
            while True:
                updateClientStatus(clientStatus)
                try:
                    message = connection.recv(1024).decode(FORMAT)

                    if message == "Sign up": handleClientSignUp(connection, nClient, clientStatus)

                    elif message == "Login": usingAccount = handleClientLogin(connection, nClient, onlineClient, clientStatus)

                    elif message == "Logout":
                        onlineClient.remove(usingAccount)
                        tmp = usingAccount + " has logged out"
                        clientStatus.append(tmp)

                    elif message == "Look up": 
                        connection.sendall(data_send.encode(FORMAT))

                    elif message == "Exit":
                        tmp = "Client " + str(nClient) + " has disconnected."
                        onlineClient.remove(usingAccount)
                        clientStatus.append(tmp)
                        updateClientStatus(clientStatus)
                        connection.close()
                        break

                except:
                    tmp = "Client " + str(nClient) + " might be forcibly disconnected!"
                    onlineClient.remove(usingAccount)
                    clientStatus.append(tmp)
                    updateClientStatus(clientStatus)
                    connection.close()
                    break

        def updateClientStatus(clientStatus):
            self.data.delete(0, len(clientStatus))
            for i in clientStatus:
                self.data.insert(clientStatus.index(i), i)
        
        def closeServer(): self.destroy()

        def runServer():
            nClient = 1
            onlineClient = []
            clientStatus = []

            while True:
                connection, address = server.accept()

                thread = threading.Thread(target = handleClient, args = (self, connection, address, nClient, onlineClient, clientStatus))
                thread.daemon = False
                thread.start()
                nClient+=1

        serverThread = threading.Thread(target = runServer)
        serverThread.daemon = False
        serverThread.start()

#initJsonFile('test.json',NUM_OF_DAY)
updateData(url, 'test.json', NUM_OF_DAY)
with open('test.json') as json_file:
        data = pandas.read_json(json_file, orient='index')
data_send=data.to_json()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

try:
    app = App()
    app.mainloop()
except:
    server.close()

