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

background_img = PhotoImage(file = f"BG_tracuu.png")
background = canvas.create_image(
    250.0, 150.0,
    image=background_img)

canvas.create_text(
    373.0, 48.5,
    text = "HOMEPAGE",
    fill = "#ffffff",
    font = ("Questrial-Regular", int(20.0)))

canvas.create_text(
    373.0, 98.5,
    text = "Currency",
    fill = "#ffffff",
    font = ("Questrial-Regular", int(12.0)))

canvas.create_text(
    371.0, 146.5,
    text = "Date",
    fill = "#ffffff",
    font = ("Questrial-Regular", int(12.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 285, y = 205,
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
    x = 384, y = 205,
    width = 76,
    height = 16)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    372.5, 120.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry0.place(
    x = 285, y = 112,
    width = 175,
    height = 15)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    372.5, 166.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 285, y = 158,
    width = 175,
    height = 15)

window.resizable(False, False)
window.mainloop()
