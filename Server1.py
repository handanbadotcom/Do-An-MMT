import tkinter as Tk
import socket
import threading
import json

import requests
import lxml
import pandas as pd
from datetime import datetime
from bs4 import BeautifulSoup
import time
import re
import os

HOSTNAME = socket.gethostname()
HOST = socket.gethostbyname(HOSTNAME)
PORT = 65432
FORMAT = "utf8"

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

        def handleClientLookUp(connection, nClient, clientStatus, usingAccount):
            url = 'https://vi.wikipedia.org/wiki/B%E1%BA%A3n_m%E1%BA%ABu:D%E1%BB%AF_li%E1%BB%87u_%C4%91%E1%BA%A1i_d%E1%BB%8Bch_COVID-19_t%E1%BA%A1i_Vi%E1%BB%87t_Nam'
            driver = webdriver.Chrome()
            driver.get(url)

            # tạo soup, tìm bảng
            time.sleep(5)
            soup = BeautifulSoup(driver.page_source, 'lxml')
            tables = soup.find(
                'table', class_='wikitable plainrowheaders sortable tpl-blanktable jquery-tablesorter')

            # hàm chuyển string thành số
            def process_num(num):
                return float(re.sub(r'[^\w\s.]', '', num))

            # lập cột
            provinces = []
            cases = []
            deaths = []
            # tìm data
            for row in tables.findAll('tr'):
                cells = row.find_all('td')
                if len(cells) > 1:
                    province = cells[0]
                    provinces.append(province.text.strip())  # lấy cột tỉnh

                    case = cells[1]
                    cases.append(process_num(case.text.strip()))  # cột ca nhiễm

                    death = cells[2]
                    deaths.append(process_num(death.text.strip()))  # cột người chết

            # lập list để tạo dataframe
            data = {'Tỉnh': provinces, 'Số ca nhiễm': cases, 'Tử vong': deaths}

            # lập data frame
            df1 = pd.DataFrame(data)
            pd.set_option('display.max_rows', 1000)

            # tìm kiếm
            name = connection.recv(1024).decode(FORMAT)
            try:
                df2 = df1.loc[df1['Tỉnh'] == name]
                df2 = df2.reset_index()

                province = df2.at[0, 'Tỉnh']  # Gán tên tỉnh cần tìm vào biến mới
                cases = df2.at[0, 'Số ca nhiễm']  # Gán biến ca nhiễm
                deaths = df2.at[0, 'Tử vong']  # Gán số liệu tử vong vào biến mới
                cases = str(cases)[0:len(str(cases)) - 2]
                deaths = str(cases)[0:len(str(cases)) - 2]


                connection.sendall('True'.encode(FORMAT))
                connection.recv(1024).decode(FORMAT)

                connection.sendall(cases.encode(FORMAT))
                connection.recv(1024).decode(FORMAT)
                connection.sendall(deaths.encode(FORMAT))
                
                tmp = "Client " + str(nClient) + " has searched for cases and deaths of: " + name
                clientStatus.append(tmp)
            except:
                connection.sendall('False'.encode(FORMAT))

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

                    elif message == "Look up": handleClientLookUp(connection, nClient, clientStatus, usingAccount)

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

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

try:
    app = App()
    app.mainloop()
except:
    server.close()

