import random 
from tkinter import *
from pathlib import Path

neuronsArr = [random.randbytes(1).hex() for i in range(3)] #initial random hexadec
hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2] #initial hexcolorcode
BASE_DIR = Path(__file__).resolve().parent


def IsPurple(): #when Yes is clicked
    CheckAndRegen(True)

def NotPurple(): #when No is Clicked
    CheckAndRegen(False)


def CheckAndRegen(isPurple):
    global neuronsArr, hexColor
    with open(BASE_DIR / "colorblinddata.csv",'a') as file:
        file.write(f"{neuronsArr[0]}, {neuronsArr[1]}, {neuronsArr[2]}, {hexColor}, {int(isPurple)}\n")
    if isPurple:
        print("yuh")
    else:
        print("nuh")
    
    neuronsArr = [random.randbytes(1).hex() for i in range(3)]
    hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2]
    canvas.itemconfigure("rect", fill=hexColor)   


root = Tk() #window setup
root.title("Color")
mainframe = Frame(root, width=256, height=384)
mainframe.grid()
canvas = Canvas(mainframe, width=256, height=128)
canvas.grid(row=0, column=0)
canvas.create_rectangle(0, 0, 256, 128, fill=hexColor, tags="rect")
buttonFrame = Frame(mainframe)
buttonFrame.grid(row=1, column=0)
bYes = Button(buttonFrame, text="Yes", command=IsPurple)
bNo = Button(buttonFrame, text="No", command=NotPurple)
bYes.grid(row=0, column=0)
bNo.grid(row=0, column=1)

root.mainloop()


