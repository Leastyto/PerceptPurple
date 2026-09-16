import random 
from tkinter import *
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def Train(learningrate = 0.1, epochs = 500, path = None): #literally pulled outa my ass i have no clue if theyre too big or too small
    print("Training...") #so i know if i actually ran the damn thing
    if path is None:
        path = BASE_DIR / "colorblinddata.csv"
    with open(path, "r") as data:
        trainingdata = []
        for line in data:
            parts = [part.strip() for part in line.strip().split(",")]
            if len(parts) < 5:
                continue

            r = int(parts[0], 16) / 255.0
            g = int(parts[1], 16) / 255.0
            b = int(parts[2], 16) / 255.0
            target = int(parts[4])
            trainingdata.append(([r, g, b], target))

    weights = [0.5, 0.5, 0.5]
    bias = 0.0

    for _ in range(epochs):
        for inputs, target in trainingdata:
            z = sum(weights[i] * inputs[i] for i in range(3)) + bias
            prediction = 1 if z > 0 else 0
            error = target - prediction

            for i in range(3):
                weights[i] += learningrate * error * inputs[i]
            bias += learningrate * error
    print(f"Returned with weights: {weights}, and bias: {bias}")
    return(weights, bias)


def CheckIt(hexcode, weights, bias): #using trained weights to make a guess
    inputs = [int(hexcode[1:3],16),int(hexcode[3:5],16),int(hexcode[5:],16)]
    z = sum(weights[i] * inputs[i] for i in range(3)) + bias
    if z>0:
        return 1
    else:
        return 0


trainTup = Train()

############################################great wall of gui#################################################################

neuronsArr = [random.randbytes(1).hex() for i in range(3)] #initial random hexadec
hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2] #initial hexcolorcode

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
        if CheckIt(hexColor,trainTup[0],trainTup[1]):
            print("clanka agree")
        else:
            print("clanka thought no")
    else:
        print("nuh")
        if CheckIt(hexColor,trainTup[0],trainTup[1]):
            print("clanka thought yes")
        else:
            print("clanka agree")   
    
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

