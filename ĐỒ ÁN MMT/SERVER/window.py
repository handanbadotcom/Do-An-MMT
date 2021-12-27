from tkinter import *


def btn_clicked():
    print("Button Clicked")


window = Tk()

window.geometry("500x500")
window.configure(bg = "#ffffff")
canvas = Canvas(
    window,
    bg = "#ffffff",
    height = 500,
    width = 500,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(file = f"background.png")
background = canvas.create_image(
    250.0, 250.0,
    image=background_img)

img0 = PhotoImage(file = f"img0.png")
b0 = Button(
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = btn_clicked,
    relief = "flat")

b0.place(
    x = 204, y = 424,
    width = 91,
    height = 31)

canvas.create_text(
    250.0, 116.5,
    text = "Waiting for Client...",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(15.0)))

canvas.create_text(
    250.0, 94.5,
    text = "Client Status",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(15.0)))

canvas.create_text(
    250.0, 73.5,
    text = "Server IP Address:\n",
    fill = "#5b34a9",
    font = ("Questrial-Regular", int(15.0)))

window.resizable(False, False)
window.mainloop()
