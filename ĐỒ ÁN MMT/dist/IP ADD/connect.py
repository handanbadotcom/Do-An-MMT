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
    355.5, 105.5,
    text = "Server IP Address",
    fill = "#ffffff",
    font = ("Questrial-Regular", int(15.0)))

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 318, y = 158,
    width = 76,
    height = 16)

entry0_img = PhotoImage(file = f"img_textBox0.png")
entry0_bg = canvas.create_image(
    355.5, 198.5,
    image = entry0_img)

entry0 = Entry(
    bd = 0,
    bg = "#7456af",
    highlightthickness = 0)

entry0.place(
    x = 293, y = 190,
    width = 125,
    height = 15)

entry1_img = PhotoImage(file = f"img_textBox1.png")
entry1_bg = canvas.create_image(
    355.5, 133.5,
    image = entry1_img)

entry1 = Entry(
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0)

entry1.place(
    x = 268, y = 125,
    width = 175,
    height = 15)

window.resizable(False, False)
window.mainloop()
