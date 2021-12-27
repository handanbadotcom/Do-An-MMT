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
    250.0, 38.5,
    text = "SIGN UP",
    fill = "#6d7589",
    font = ("Quando-Regular", int(20.0)))

canvas.create_text(
    250.0, 66.5,
    text = "Username",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(12.0)))

canvas.create_text(
    250.0, 115.5,
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
    x = 162, y = 232,
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
    x = 261, y = 232,
    width = 76,
    height = 16)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    250.0, 211.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#d6cee7",
    highlightthickness = 0)

entry0.place(
    x = 56, y = 201,
    width = 388,
    height = 19)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    249.5, 86.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 162, y = 78,
    width = 175,
    height = 15)

entry2_img = PhotoImage(file = f"img_textBox2.png")
entry2_bg = canvas.create_image(
    249.5, 135.5,
    image = entry2_img)

entry2 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry2.place(
    x = 162, y = 127,
    width = 175,
    height = 15)

canvas.create_text(
    250.0, 162.5,
    text = "Confirm Password",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(12.0)))

entry3_img = PhotoImage(file = f"img_textBox3.png")
entry3_bg = canvas.create_image(
    249.5, 182.5,
    image = entry3_img)

entry3 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry3.place(
    x = 162, y = 174,
    width = 175,
    height = 15)

window.resizable(False, False)
window.mainloop()
