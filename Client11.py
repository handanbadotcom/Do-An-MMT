import tkinter as Tk
from tkinter import messagebox
import socket

HOST = ""
PORT = 65432
FORMAT = "utf8"

class ConnectPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        titleLabel = Tk.Label(self, text = 'CONNECT')
        serverIPLabel = Tk.Label(self, text = 'Server IP Address:')
        self.serverIPEntry = Tk.Entry(self)
        self.notifyLabel = Tk.Label(self, text = '')
        connectButton = Tk.Button(self, text = 'Connect', command=lambda: appControl.Connect(self, client))

        titleLabel.pack()
        serverIPLabel.pack()
        self.serverIPEntry.pack()
        self.notifyLabel.pack()
        connectButton.pack()

class SignInPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        titleLabel = Tk.Label(self, text = 'SIGN IN')
        usernameLabel = Tk.Label(self, text = 'Username:')
        self.usernameEntry = Tk.Entry(self)
        passwordLabel = Tk.Label(self, text = 'Password:')
        self.passwordEntry = Tk.Entry(self, show = '*')
        self.notifyLabel = Tk.Label(self, text = '')
        loginButton = Tk.Button(self, text = 'Login', command=lambda: appControl.Login(self, client))
        signUpButton = Tk.Button(self, text = 'Sign up', command=lambda: appControl.showPage(SignUpPage))
        exitButton = Tk.Button(self, text = 'Exit', command=lambda: appControl.Exit())

        titleLabel.pack()
        usernameLabel.pack()
        self.usernameEntry.pack()
        passwordLabel.pack()
        self.passwordEntry.pack()
        self.notifyLabel.pack()
        loginButton.pack()
        signUpButton.pack()
        exitButton.pack()

class SignUpPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        titleLabel = Tk.Label(self, text = 'SIGN UP')
        usernameLabel = Tk.Label(self, text = 'Username:')
        self.usernameEntry = Tk.Entry(self)
        passwordLabel = Tk.Label(self, text = 'Password:')
        self.passwordEntry = Tk.Entry(self, show = '*')
        confirmPasswordLabel = Tk.Label(self, text = 'Confirm Password:')
        self.confirmPasswordEntry = Tk.Entry(self, show = '*')
        self.notifyLabel = Tk.Label(self, text = '')
        signUpButton = Tk.Button(self, text = 'Sign up', command=lambda: appControl.signUp(self, client))
        backButton = Tk.Button(self, text = 'Back', command=lambda: appControl.showPage(SignInPage))

        titleLabel.pack()
        usernameLabel.pack()
        self.usernameEntry.pack()
        passwordLabel.pack()
        self.passwordEntry.pack()
        confirmPasswordLabel.pack()
        self.confirmPasswordEntry.pack()
        self.notifyLabel.pack()
        signUpButton.pack()
        backButton.pack()

class HomePage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        titleLabel = Tk.Label(self, text = 'HOME PAGE')
        logoutButton = Tk.Button(self, text = 'Logout', command=lambda: appControl.Logout())
        titleLabel.pack()
        logoutButton.pack()

class App(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)

        self.title("Client")
        self.geometry("400x300")
        self.resizable(width = False, height = False)

        container = Tk.Frame()
        container.pack(side = 'top', fill = 'both', expand = True)
        container.grid_rowconfigure(0, weight = 1)
        container.grid_columnconfigure(0, weight = 1)

        self.frames = {}
        for f in (ConnectPage, SignInPage, HomePage, SignUpPage):
            frame = f(container, self)
            frame.grid(row = 0, column = 0, sticky = 'nsew')
            self.frames[f] = frame

        self.frames[ConnectPage].tkraise()

    def showPage(self, page): self.frames[page].tkraise()

    def Connect(self, currentPage, client):
        HOST = currentPage.serverIPEntry.get()
        print("You tried to connect to Server:", HOST, PORT)
        try: 
            client.connect((HOST, PORT))
            print("Successfully Connected")
            print("Your Address:", client.getsockname())            
            self.showPage(SignInPage)
                
        except:
            print("Failed to Connect!")
            currentPage.notifyLabel['text'] = "Invalid IP Address"

    def signUp(self, currentPage, client):
        try:
            username = currentPage.usernameEntry.get()
            password = currentPage.passwordEntry.get()
            confirmPassword = currentPage.confirmPasswordEntry.get()

            if username == "" or password == "" or confirmPassword == "":
                currentPage.notifyLabel['text'] = "You must fill all the empty fields!"
                return

            print("You tried to sign up with username:", username, "- password:", password, "- confirm password:", confirmPassword)

            if confirmPassword != password:
                currentPage.notifyLabel['text'] = "Your password and confirm password don't match!"
                print("Failed to Sign up")
                return

            client.sendall('Sign up'.encode(FORMAT))

            client.sendall(username.encode(FORMAT))

            response = client.recv(1024).decode(FORMAT)
            if response == 'False':
                currentPage.notifyLabel['text'] = "This username already exists, please try again!"
                print("Failed to Sign up")
                return

            client.sendall(password.encode(FORMAT))

            print("Successfully Signed up")

            self.showPage(SignInPage)

            self.frames[SignInPage].notifyLabel['text'] = "Successfully Signed up! Use your account to login"

            self.frames[SignUpPage].notifyLabel['text'] = ""

        except:
            self.Error()

    def Login(self, currentPage, client):
        try:
            client.sendall('Login'.encode(FORMAT))

            username = currentPage.usernameEntry.get()
            password = currentPage.passwordEntry.get()

            if username == "" or password == "":
                currentPage.notifyLabel['text'] = "You must fill all the empty fields!"
                return

            print("You tried to login with username:", username, "- password:", password)

            client.sendall(username.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(password.encode(FORMAT))

            response = client.recv(1024).decode(FORMAT)
            if response == 'True':
               self.showPage(HomePage)
               return
            if response == 'Exist':
               currentPage.notifyLabel['text'] = "This account is already logged in by another client!"
               print("Failed to Login")
               return
            else: 
               currentPage.notifyLabel['text'] = "Your username or password is incorrect, please try again!"
               print("Failed to Login")
               return

            self.frames[SignInPage].notifyLabel['text'] = ''               
        except:
            self.Error()

    def Logout(self):
        try:
            client.sendall('Logout'.encode(FORMAT))
            self.showPage(SignInPage)
            print("Logged out!")
        except: self.Error()

    def Exit(self):
        try: 
            client.sendall('Exit'.encode(FORMAT))
            self.destroy()
        except: self.Error()
        
    def Error(self):
        messagebox.showerror('Server Error', 'Error: Server has been closed!');
        self.destroy()


client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

app = App()
app.mainloop()

client.close()
