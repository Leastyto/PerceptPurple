import random 
from tkinter import *
from pathlib import Path

#paths
BASE_DIR = Path(__file__).resolve().parent
splashpath = BASE_DIR / "perceptpurple.png"
trainpath = BASE_DIR /  "train.png"
comppath = BASE_DIR / "compare.png"

#initial random color setup
neuronsArr = [random.randbytes(1).hex() for i in range(3)] #initial random hexadec
hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2] #initial hexcolorcode

#main window setup
root = Tk()
root.title("PerceptPurple")
root.geometry("512x340") 
root.resizable(False,False)
root.configure(background="#1c0030")

#window frame
mainframe = Frame(root, width=512, height=340, background="#1c0030")
mainframe.grid()
mainframe.grid_columnconfigure(0, weight=1)

#splash screen
canvas = Canvas(mainframe,bd=0,highlightthickness=0, width=512, height=200)
canvas.grid(row=0,column=0)
splash = PhotoImage(file=splashpath)
canvas.create_image(0,0, image=splash, anchor = "nw")

#button frame
buttonframe = Frame(mainframe,width=512, height=60, bg="#1c0030", bd=0, highlightthickness=0)
buttonframe.grid(row=1,column=0, sticky="nsew")
buttonframe.grid_columnconfigure(0, weight=1)
buttonframe.grid_columnconfigure(1, weight=1)

#button funcs
def TrainButton():
    Training(hexColor)

def CompareButton():
    Comparing()


#train button
trainimg = PhotoImage(file=trainpath)
btrain = Button(buttonframe, image=trainimg, bg="#1c0030", activebackground="#1c0030", bd=0, highlightthickness=0, padx=0, pady=0, command=TrainButton)
btrain.grid(row=0, column=0, sticky="nsew", padx=0, pady=10)

#compare button
compimg = PhotoImage(file=comppath)
bcompare = Button(buttonframe, image=compimg, bg="#1c0030", activebackground="#1c0030", bd=0, highlightthickness=0, padx=0, pady=0)
bcompare.grid(row=0,column=1, sticky="nsew", padx=0, pady=10)

def Training(hexColor):
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
        
        neuronsArr = [random.randbytes(1).hex() for _ in range(3)]
        hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2]
        colorrect.itemconfigure("rect", fill=hexColor)   

    trainwindow = Toplevel(root)
    trainwindow.title("Training...")
    trainframe = Frame(trainwindow, width=256, height=384)
    trainframe.grid()
    colorrect = Canvas(trainframe, width=256, height=128)
    colorrect.grid(row=0, column=0)
    colorrect.create_rectangle(0, 0, 256, 128, fill=hexColor, tags="rect")
    choiceframe = Frame(trainframe)
    choiceframe.grid(row=1, column=0)
    bYes = Button(choiceframe, text="Yes", command=IsPurple)
    bNo = Button(choiceframe, text="No", command=NotPurple)
    bYes.grid(row=0, column=0)
    bNo.grid(row=0, column=1)   

def Comparing():
    pass #not done yet, can't copy paste previous code here and it's 1:35 am

root.mainloop()