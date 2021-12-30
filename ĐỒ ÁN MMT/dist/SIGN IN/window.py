from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("500x300")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 300,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    250.0, 150.0,
    image=background_img)

canvas.create_text(
    250.0, 103.5,
    text = "Username",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(12.0)))

canvas.create_text(
    250.0, 151.5,
    text = "Password",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(12.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 165, y = 229,
    width = 76,
    height = 16)

img1 = PhotoImage(file = f"img1.png")
b1 = Button(
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b1.place(
    x = 264, y = 229,
    width = 76,
    height = 16)

img2 = PhotoImage(file = f"img2.png")
b2 = Button(
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b2.place(
    x = 215, y = 257,
    width = 76,
    height = 16)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    253.0, 204.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d6cee7",
    highlightthickness = 0)

entry0.place(
    x = 34, y = 191,
    width = 438,
    height = 25)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    249.5, 125.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 162, y = 117,
    width = 175,
    height = 15)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    249.5, 172.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 162, y = 164,
    width = 175,
    height = 15)

canvas.create_text(
    250.0, 72.0,
    text = "LOGIN",
    fill = "#6d7589",
    font = ("Quando-Regular", int(20.0)))

window.resizable(False, False)
window.mainloop()
