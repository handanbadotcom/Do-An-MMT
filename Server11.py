import tkinter as Tk
import socket
import threading
import json

HOSTNAME = socket.gethostname()
HOST = '127.0.0.1'#socket.gethostbyname(HOSTNAME)
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
        waitingLabel = Tk.Label(self, text = 'Waiting for Client...').pack()

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

        def handleClient(connection, address, nClient, onlineClient, clientStatus):
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

                    elif message == "Exit":
                        tmp = "Client " + str(nClient) + " has disconnected."
                        clientStatus.append(tmp)
                        updateClientStatus(clientStatus)
                        connection.close()
                        break

                except:
                    tmp = "Client " + str(nClient) + " might be forcibly disconnected!"
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
                thread = threading.Thread(target = handleClient, args = (connection, address, nClient, onlineClient, clientStatus))
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

