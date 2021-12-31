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
import time
import tkinter.scrolledtext as st

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 60090
FORMAT = "utf8"
NUM_OF_DAY = 3 

Limit = 30      #phut
url = 'https://sbv.gov.vn/TyGia/faces/TyGiaMobile.jspx?_afrLoop=14339020310096506&_afrWindowMode=0&_adf.ctrl-state=1786p90txj_21'
fileName='Currency.json'
account_fileName='account.json'

def checkAccount(fileName, ID, pw):
    with open(fileName) as json_file:
        DF = pandas.read_json(json_file, orient='index')
    n = int(DF.size /2)
    for i in range(0,n):
        if DF.iat[i,0] == ID and DF.iat[i, 1] == pw:
            return True
    return False
def checkID(fileName, ID):
    with open(fileName) as json_file:
        DF = pandas.read_json(json_file, orient='index')
    n = int(DF.size /2)
    for i in range(0,n):
        if DF.iat[i,0] == ID:
            return False
    return True
def addAccount(fileName, ID, pw):
    with open(fileName) as json_file:
        DF = pandas.read_json(json_file, orient='index')
    n = int(DF.size /2)
    struct = {'ID':pandas.Series(ID,index = [n]),
          'pass':pandas.Series(pw,index= [n])}
    newDF = pandas.DataFrame(struct)
    DF = pandas.concat([DF, newDF], axis=0, join='inner')
    with open(fileName, 'w+') as file:
        DF.to_json(file, orient='index')
def initAccountFile(tenFile):
    try:
        with open(tenFile) as json_file:
            TMP = pandas.read_json(json_file, orient='index')
        return
    except:
        struct = {'ID':pandas.Series(''),
            'pass':pandas.Series('')}
        DF = pandas.DataFrame(struct)
        with open(tenFile, 'w+') as file:
            DF.to_json(file, orient='index')
def openFile(Filename):
    with open(Filename) as json_file:
        data = pandas.read_json(json_file, orient='index')
    return data    
def initJsonFile(tenFile, NumOfDay): 
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
    try:
        with open(fileName) as json_file:
            data = pandas.read_json(json_file, orient='index')
        now = datetime.datetime.now()
        today=now.strftime("%d/%m/%Y")
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
    except:
        initJsonFile(fileName,NumOfDay)
        updateData(url,fileName,NumOfDay)
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

        self.canvas = Tk.Canvas(self,bg = "#ffffff",height = 500,width = 500,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = Tk.PhotoImage(file = f"SERVER\BG_server.png")
        self.canvas.create_image(250.0, 250.0,image=self.background_img)

        self.canvas.create_text(250.0, 45, text = "Server IP Address:" +HOST, fill = "#5b34a9", font = ("Questrial-Regular", int(10.0)))
        self.canvas.create_text(250.0, 70,text = "Client Status",fill = "#5b34a9",font = ("Questrial-Regular", int(15.0)))

        self.data =st.ScrolledText(self, height= 20, width= 42)     
        self.data.place(x = 75, y =90)

        self.img0 = Tk.PhotoImage(file = f"SERVER\img0_server.png")
        self.b0 = Tk.Button(self,image = self.img0,borderwidth = 0,highlightthickness = 0, command = self.destroy ,relief = "flat")
        self.b0.place(x = 204, y = 424,width = 91,height = 31)
        
        def handleClientSignUp(connection, nClient, clientStatus):

            ID = connection.recv(1024).decode(FORMAT)
            tmp = checkID(account_fileName,ID)
            if tmp:
                connection.sendall(str(tmp).encode(FORMAT))
                pw=connection.recv(1024).decode(FORMAT)
                addAccount(account_fileName,ID,pw)
            else:
                connection.sendall(str(tmp).encode(FORMAT))

            tmp = "Client " + str(nClient) + " has signed up with username: " + ID
            clientStatus.append(tmp)


        def handleClientLogin(connection, nClient, onlineClient, clientStatus):
            ID = connection.recv(1024).decode(FORMAT)
            connection.sendall(ID.encode(FORMAT))
            pw = connection.recv(1024).decode(FORMAT)
            
            check = checkAccount(account_fileName,ID,pw)
            if ID in onlineClient:
                connection.sendall('Exist'.encode(FORMAT))
            else:
                connection.sendall(str(check).encode(FORMAT))

            if check:
                onlineClient.append(ID)
                tmp = "Client " + str(nClient) + " has logged in as: " + ID
                clientStatus.append(tmp)
            return ID
            #clientAccount = {"username": ID, "password": pw}

        def handleClient(self, connection, address, nClient, onlineClient, clientStatus):
            
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
                        if usingAccount in onlineClient: onlineClient.remove(usingAccount)
                        clientStatus.append(tmp)
                        updateClientStatus(clientStatus)
                        connection.close()
                        break
                    elif message=='': raise Exception
                except:
                    tmp = "Client " + str(nClient) + " might be forcibly disconnected!"
                    if usingAccount in onlineClient: onlineClient.remove(usingAccount)
                    clientStatus.append(tmp)
                    updateClientStatus(clientStatus)
                    connection.close()
                    break

        def updateClientStatus(clientStatus):
            self.data.delete('1.0', Tk.END)
            for i in clientStatus:
                self.data.insert(Tk.INSERT,i+'\n')
    
        
        

        def runServer():
            nClient = 1
            onlineClient = []
            clientStatus = []
            while True:
                connection, address = server.accept()
                thread = threading.Thread(target = handleClient, args = (self, connection, address, nClient, onlineClient, clientStatus))
                thread.daemon = True
                thread.start()
                nClient+=1


        serverThread = threading.Thread(target = runServer)
        serverThread.daemon = True
        serverThread.start()

initAccountFile(account_fileName)
updateData(url, fileName, NUM_OF_DAY)
data_send=openFile(fileName).to_json()
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

def timeCounter():
    global data_send
    while True:
        time.sleep(60 * Limit)
        updateData(url, fileName, NUM_OF_DAY)
        data_send=openFile(fileName).to_json()
        
t = threading.Thread(target = timeCounter)
t.daemon=True
t.start()

try:
    app = App()
    app.mainloop()
except:
    server.close()

