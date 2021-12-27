import tkinter as Tk
from tkinter import messagebox
import socket
import pandas
import tkinter.scrolledtext as st
HOST = ""
PORT = 60090
FORMAT = "utf8"
def pw_check(pw):
      
    SpecialSym =['!', '@', '#', '$', '%', '^', '&', '*']
    level = 0  
    value='True'
    if len(pw) < 6:
        value='length should be at least 6'
        return value
          
    if len(pw) > 20:
        value='length should be not be greater than 20'
        return value
          
    if any(char.isdigit() for char in pw):
        level += 1
          
    if any(char.isupper() for char in pw):
        level += 1
          
    if any(char.islower() for char in pw):
        level += 1
          
    if any(char in SpecialSym for char in pw):
        level += 1

    if level < 3:
        value='Password should have at least 3 of things: numberal, uppercase \n lowercase, letter, special symbol(!, @, #, $, %, ^, &, *)!!!'
    return value
def search_currency(data, find):
    f=''
    for i in data:
        if data[i]["Ngo\u1ea1i t\u1ec7"]==find:  
          f=f+str(data[i].map(str))
          f=f+'\n'
          tmp = 'Name: ' + str(i) + ', dtype: object'
          f = f.replace(tmp,'')
    return(f)
def search_date(data, date):
    f=''
    for i in data:
        if data[i]["Ng\u00e0y"]==date:
            f=f+str(data[i].map(str)) #print(data[i])
            f=f+ '\n'
            tmp = 'Name: ' + str(i) + ', dtype: object'
            f = f.replace(tmp,'')
    return(f)
def search(data, currency=None, date=None):
    f=''
    if date=='':
      return( search_currency(data,currency))
    if currency=='':
        return(search_date(data,date))
    else:    
        for i in data:
            if (data[i]["Ngo\u1ea1i t\u1ec7"]==currency) and (data[i]["Ng\u00e0y"]==date):
                f=f+str(data[i].map(str)) #print(data[i])
                f=f+ '\n'
                tmp = 'Name: ' + str(i) + ', dtype: object'
                f = f.replace(tmp,'')
    return(f)

class ConnectPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self,bg = "#ffffff",height = 300,width = 500,bd = 0,highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = Tk.PhotoImage(file = f"IP ADD\BG_connect.png")
        self.canvas.create_image(250.0, 150.0,image=self.background_img)

        self.canvas.create_text(355.5, 105.5,text = "Server IP Address",fill = "#ffffff",font = ("Questrial-Regular", int(15.0)))

        self.entry1_img = Tk.PhotoImage(file = f"IP ADD\img_textBox1_connect.png") #TextBox_Connect
        self.canvas.create_image(355.5, 133.5,image = self.entry1_img)
        self.serverIPEntry = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.serverIPEntry.place( x = 268, y = 125, width = 175, height = 15)

        self.notify=self.canvas.create_text(355.5, 200, text = "", fill = "#5b34a9", font = ("Questrial-Regular", int(12.0))) # Notify

        self.img0 = Tk.PhotoImage(file = f"IP ADD\img0_connect.png") #Button_Connect
        self.b0 = Tk.Button(self,image = self.img0,borderwidth = 0,highlightthickness = 0, command=lambda:appControl.Connect(self,client),relief = "flat")
        self.b0.place(x = 318, y = 158,width = 76,height = 16)

        
class SignInPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)
        self.canvas = Tk.Canvas(self,bg = "#ffffff", height = 300, width = 500, bd = 0, highlightthickness = 0, relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.background_img = Tk.PhotoImage(file = f"SIGN IN\BG_signin.png")
        self.canvas.create_image(250.0, 150.0, image=self.background_img)
         
        self.canvas.create_text(250.0, 72.0,text = "LOGIN",fill = "#6d7589",font = ("Quando-Regular", int(20.0))) #Login

        self.canvas.create_text(250.0, 103.5,text = "Username",fill = "#5b34a9", font = ("Questrial-Regular", int(12.0))) #Username
        self.entry1_img = Tk.PhotoImage(file = f"SIGN IN\img_textBox1_signin.png") #TextBox_Username
        self.canvas.create_image( 249.5, 125.5,  image = self.entry1_img)
        self.entry1 = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.entry1.place( x = 162, y = 117, width = 175, height = 15)

        self.canvas.create_text(250.0, 151.5,text = "Password",fill = "#5b34a9", font = ("Questrial-Regular", int(12.0))) #Pass
        self.entry2_img = Tk.PhotoImage(file = f"SIGN IN\img_textBox2_signin.png") #TextBox_Pass
        self.canvas.create_image( 249.5, 172.5,  image = self.entry2_img)
        self.entry2 = Tk.Entry(self, bd = 0, bg = "#ffffff", highlightthickness = 0, show = '*')
        self.entry2.place( x = 162, y = 164, width = 175, height = 15)

        self.img0 = Tk.PhotoImage(file = f"SIGN IN\img0_signin.png")
        self.b0 = Tk.Button(self,image = self.img0,borderwidth = 0,highlightthickness = 0, command =lambda:appControl.Login(self, client), relief = "flat")
        self.b0.place(x = 165, y = 229,width = 76,height = 16)

        self.img1 = Tk.PhotoImage(file = f"SIGN IN\img1_signin.png")
        self.b1 = Tk.Button(self,image = self.img1,borderwidth = 0,highlightthickness = 0, command =lambda:appControl.showPage(SignUpPage), relief = "flat")
        self.b1.place(  x = 264, y = 229, width = 76, height = 16)

        self.img2 = Tk.PhotoImage(file = f"SIGN IN\img2_signin.png")
        self.b2 = Tk.Button(self,image = self.img2,borderwidth = 0,highlightthickness = 0,command =lambda:appControl.Exit(),relief = "flat")
        self.b2.place(x = 215, y = 257, width = 76, height = 16)

        self.notify=self.canvas.create_text(250, 200, text = "", fill = "#5b34a9", font = ("Questrial-Regular", int(12.0))) # Notify
class SignUpPage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self,bg = "#ffffff",height = 300,width = 500,bd = 0,highlightthickness = 0,relief = "ridge")
        self.canvas.place(x = 0, y = 0)  

        self.background_img = Tk.PhotoImage(file = f"SIGN UP\BG_signup.png")
        self.canvas.create_image(250.0, 150.0,image=self.background_img)

        self.canvas.create_text(250.0, 38.5,text = "SIGN UP",fill = "#6d7589",font = ("Quando-Regular", int(20.0)))

        self.canvas.create_text(250.0, 66.5,text = "Username",fill = "#5b34a9",font = ("Questrial-Regular", int(12.0)))

        self.entry1_img = Tk.PhotoImage(file = f"SIGN UP\img_textBox1_signup.png") #TextBox_Signup
        self.canvas.create_image(250, 86.5,image = self.entry1_img)
        self.entry1 = Tk.Entry(self, bd = 0,bg = "#ffffff",highlightthickness = 0)
        self.entry1.place(x = 162, y = 78, width = 175, height = 15)

        self.canvas.create_text(250.0, 115.5, text = "Password",fill = "#5b34a9",font = ("Questrial-Regular", int(12.0))) #TextBox_Pass
        self.entry2_img = Tk.PhotoImage(file = f"SIGN UP\img_textBox2_signup.png")
        self.canvas.create_image(249.5, 135.5, image = self.entry2_img)
        self.entry2 = Tk.Entry(self, bd = 0, bg = "#ffffff",highlightthickness = 0,show = '*')
        self.entry2.place(x = 162, y = 127, width = 175,height = 15)

        self.canvas.create_text(250.0, 162.5,text = "Confirm Password",fill = "#5b34a9",font = ("Questrial-Regular", int(12.0))) #TextBox_ConfirmPass
        self.entry3_img = Tk.PhotoImage(file = f"SIGN UP\img_textBox3_signup.png")
        self.canvas.create_image(249.5, 182.5,image = self.entry3_img)
        self.entry3 = Tk.Entry(self, bd = 0,bg = "#ffffff", highlightthickness = 0,show = '*')
        self.entry3.place( x = 162, y = 174, width = 175, height = 15)

        self.img0 = Tk.PhotoImage(file = f"SIGN UP\img0_signup.png") #Button_SignUp
        self.b0 = Tk.Button(self,image = self.img0,borderwidth = 0,highlightthickness = 0,command = lambda:appControl.signUp(self, client),relief = "flat")
        self.b0.place(x = 162, y = 232, width = 76, height = 16)

        self.img1 = Tk.PhotoImage(file = f"SIGN UP\img1_signup.png") #Button_Back
        self.b1 = Tk.Button(self,image = self.img1, borderwidth = 0, highlightthickness = 0, command = lambda:appControl.showPage(SignInPage), relief = "flat")
        self.b1.place(x = 261, y = 232,width = 76, height = 16)

        self.notify=self.canvas.create_text(250, 210, text = "", fill = "#5b34a9", font = ("Questrial-Regular", int(12.0))) # Notify
class HomePage(Tk.Frame):
    def __init__(self, parent, appControl):
        Tk.Frame.__init__(self, parent)

        self.canvas = Tk.Canvas(self,bg = "#ffffff",height = 300,width = 500, bd = 0, highlightthickness = 0,relief = "ridge")
        self.canvas.place(x = 0, y = 0)

        self.backgroundImg = Tk.PhotoImage(file = f"TRACUU\BG_tracuu.png")
        self.canvas.create_image(250.0, 150.0,image=self.backgroundImg)

        self.canvas.create_text(373.0, 48.5,  text = "HOMEPAGE",fill = "#ffffff",font = ("Questrial-Regular", int(20.0)))

        self.canvas.create_text(373.0, 98.5,text = "Currency", fill = "#ffffff", font = ("Questrial-Regular", int(12.0))) #TextBox Currency
        self.entry0_img = Tk.PhotoImage(file = f"TRACUU\img_textBox0_tracuu.png")
        self.canvas.create_image(372.5, 120.5,image = self.entry0_img)
        self.entry0 = Tk.Entry(self,bd = 0, bg = "#ffffff", highlightthickness = 0)
        self.entry0.place( x = 285, y = 112,width = 175,height = 15) 
       
        self.canvas.create_text( 371.0, 146.5, text = "Date",fill = "#ffffff", font = ("Questrial-Regular", int(12.0))) #TextBox Date
        self.entry1_img = Tk.PhotoImage(file = f"TRACUU\img_textBox1_tracuu.png")
        self.canvas.create_image(372.5, 166.5, image = self.entry1_img)
        self.entry1 = Tk.Entry(self,bd = 0,bg = "#ffffff",highlightthickness = 0)
        self.entry1.place(x = 285, y = 158, width = 175, height = 15)

        self.img0 = Tk.PhotoImage(file = f"TRACUU\img0_tracuu.png") #Lookup Button
        self.b0 = Tk.Button(self,image = self.img0, borderwidth = 0,highlightthickness = 0, command = lambda:appControl.lookUp(self, client),  relief = "flat") 
        self.b0.place( x = 285, y = 205, width = 76, height = 16)

        self.img1 = Tk.PhotoImage(file = f"TRACUU\img1_tracuu.png") #Logout Button
        self.b1 = Tk.Button(self,image = self.img1, borderwidth = 0,highlightthickness = 0, command = lambda:appControl.Logout(),  relief = "flat") 
        self.b1.place( x = 384, y = 205, width = 76, height = 16)
        
        self.notify=self.canvas.create_text(373, 190, text = "", fill = "#ffffff", font = ("Questrial-Regular", int(12.0))) #Invalid Notify

        self.text_area = st.ScrolledText(self,width = 28, height = 16)
        self.text_area.place(x = 17, y = 20)
class App(Tk.Tk):
    def __init__(self):
        Tk.Tk.__init__(self)

        self.title("Client")
        self.geometry("500x300")
        self.configure(bg="#ffffff")
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
            #currentPage.notify['text'] = "Invalid IP Address"
            currentPage.canvas.itemconfigure(currentPage.notify, text = "Invalid IP Address")

    def signUp(self, currentPage, client):
        try:
            username = currentPage.entry1.get()
            password = currentPage.entry2.get()
            confirmPassword = currentPage.entry3.get()

            if username == "" or password == "" or confirmPassword == "":
                #currentPage.notify['text'] = "You must fill all the empty fields!"
                currentPage.canvas.itemconfigure(currentPage.notify, text = "You must fill all the empty fields!")
                return

            print("You tried to sign up with username:", username, "- password:", password, "- confirm password:", confirmPassword)

            if confirmPassword != password:
                #currentPage.notify['text'] = "Your password and confirm password don't match!"
                currentPage.canvas.itemconfigure(currentPage.notify, text = "Your password and confirm password don't match!")
                print("Failed to Sign up")
                return

            tmp=pw_check(password)
            if tmp!='True':
                #currentPage.notify['text']=tmp
                currentPage.canvas.itemconfigure(currentPage.notify, text = tmp)
                return

            client.sendall('Sign up'.encode(FORMAT))
            client.sendall(username.encode(FORMAT))
            response = client.recv(1024).decode(FORMAT)
            
            if response == 'False':
                #currentPage.notify['text'] = "This username already exists, please try again!"
                currentPage.canvas.itemconfigure(currentPage.notify, text = "This username already exists, please try again!")
                print("Failed to Sign up")
                return
            else:
                client.sendall(password.encode(FORMAT))
                print("Successfully Signed up")
                self.showPage(SignInPage)
                #self.frames[SignInPage].notify['text'] = "Successfully Signed up! Use your account to login"
                #self.frames[SignUpPage].notify['text'] = ""
                currentPage.canvas.itemconfigure(currentPage.notify, text = "Successfully Signed up! Use your account to login")
                currentPage.canvas.itemconfigure(currentPage.notify, text = "")
   

        except:
            self.Error()

    def Login(self, currentPage, client):
        try:
            client.sendall('Login'.encode(FORMAT))

            username = currentPage.entry1.get()
            password = currentPage.entry2.get()

            if username == "" or password == "":
                #currentPage.notify['text'] = "You must fill all the empty fields!"
                currentPage.canvas.itemconfigure(currentPage.notify, text = "You must fill all the empty fields!")
                return

            print("You tried to login with username:", username, "- password:", password)

            client.sendall(username.encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(password.encode(FORMAT))

            response = client.recv(1024).decode(FORMAT)
            if response == 'True':
               self.showPage(HomePage)
               #self.frames[SignInPage].notify['text'] = ''   
               currentPage.canvas.itemconfigure(currentPage.notify, text = '')            
               return

            if response == 'Exist':
               #currentPage.notify['text'] = "This account is already logged in by another client!"
               currentPage.canvas.itemconfigure(currentPage.notify, text = "This account is already logged in by another client!")
               print("Failed to Login")
               return
            else: 
               #currentPage.notify['text'] = "Your username or password is incorrect, please try again!"
               currentPage.canvas.itemconfigure(currentPage.notify, text = "Your username or password is incorrect, please try again!")
               print("Failed to Login")
               return

        except:
            self.Error()

    def Logout(self):
        try:
            client.sendall('Logout'.encode(FORMAT))
            self.showPage(SignInPage)
            print("Logged out!")
        except: self.Error()

    def lookUp(self, currentPage, client):
        try:
            client.sendall('Look up'.encode(FORMAT))
            date = currentPage.entry1.get()
            currency = currentPage.entry0.get()
            response = client.recv(2048).decode(FORMAT)
            response = pandas.read_json(response, orient='index')
            data=search(response,currency,date)
            currentPage.text_area.configure(state='normal')
            currentPage.text_area.delete('1.0', Tk.END)
            currentPage.text_area.insert(Tk.INSERT,data)
            currentPage.text_area.configure(state='disabled')
        except:
            self.Error()

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
