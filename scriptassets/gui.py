import random 
from tkinter import *
from pathlib import Path

#paths
BASE_DIR = Path(__file__).resolve().parent.parent
splashpath = BASE_DIR / "imgassets" / "perceptpurple.png"
trainpath = BASE_DIR / "imgassets" /  "train.png"
comppath = BASE_DIR / "imgassets" / "compare.png"

#initial random color setup
neuronsArr = [random.randbytes(1).hex() for i in range(3)] #initial random hexadec
hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2] #initial hexcolorcode

#logic funcs
def TrainModel(learningrate = 0.1, epochs = 500, path = None): #literally pulled outa my ass i have no clue if theyre too big or too small
    print("Training...") #so i know if i actually ran the damn thing
    if path is None:
        path = BASE_DIR / "data" /  "colorblinddata.csv"
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
    traintuple = TrainModel()
    Comparing(traintuple)

def Training(hexColor):
    def IsPurple(): #when Yes is clicked
        WriteAndRegen(True)

    def NotPurple(): #when No is Clicked
        WriteAndRegen(False)

    def WriteAndRegen(isPurple):
        global neuronsArr, hexColor
        with open(BASE_DIR / "data" /"colorblinddata.csv",'a') as file:
            file.write(f"{neuronsArr[0]}, {neuronsArr[1]}, {neuronsArr[2]}, {hexColor}, {int(isPurple)}\n")
        neuronsArr = [random.randbytes(1).hex() for _ in range(3)]
        hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2]
        tcolorrect.itemconfigure("trect", fill=hexColor)
   
    trainwindow = Toplevel(root)
    trainwindow.title("Training...")
    trainframe = Frame(trainwindow, width=256, height=384)
    trainframe.grid()
    tcolorrect = Canvas(trainframe, width=256, height=128)
    tcolorrect.grid(row=0, column=0)
    tcolorrect.create_rectangle(0, 0, 256, 128, fill=hexColor, tags="trect")
    tchoiceframe = Frame(trainframe)
    tchoiceframe.grid(row=1, column=0)
    tbYes = Button(tchoiceframe, text="Yes", command=IsPurple)
    tbNo = Button(tchoiceframe, text="No", command=NotPurple)
    tbYes.grid(row=0, column=0)
    tbNo.grid(row=0, column=1)   

def Comparing(traintuple):
    def IsPurple(): #when Yes is clicked
        CheckAndRegen(True)

    def NotPurple(): #when No is Clicked
        CheckAndRegen(False)

    def CheckAndRegen(isPurple):
        global neuronsArr, hexColor
        with open(BASE_DIR / "data" /"colorblinddata.csv",'a') as file:
            file.write(f"{neuronsArr[0]}, {neuronsArr[1]}, {neuronsArr[2]}, {hexColor}, {int(isPurple)}\n")
        if isPurple:
            print("yuh")
            if CheckIt(hexColor, traintuple[0], traintuple[1]):
                print("clanka agree")
            else:
                print("clanka thought no")
        else:
            print("nuh")
            if CheckIt(hexColor, traintuple[0], traintuple[1]):
                print("clanka thought yes")
            else:
                print("clanka agree")           
        neuronsArr = [random.randbytes(1).hex() for _ in range(3)]
        hexColor = "#"+neuronsArr[0]+neuronsArr[1]+neuronsArr[2]
        ccolorrect.itemconfigure("crect", fill=hexColor)   

    compwindow = Toplevel(root)
    compwindow.title("Comparing...")
    compframe = Frame(compwindow, width=256, height=384)
    compframe.grid()
    ccolorrect = Canvas(compframe, width=256, height=128)
    ccolorrect.grid(row=0, column=0)
    ccolorrect.create_rectangle(0, 0, 256, 128, fill=hexColor, tags="crect")
    cchoiceframe = Frame(compframe)
    cchoiceframe.grid(row=1, column=0)
    cbYes = Button(cchoiceframe, text="Yes", command=IsPurple)
    cbNo = Button(cchoiceframe, text="No", command=NotPurple)
    cbYes.grid(row=0, column=0)
    cbNo.grid(row=0, column=1)  

#train button
trainimg = PhotoImage(file=trainpath)
btrain = Button(buttonframe, image=trainimg, bg="#1c0030", activebackground="#1c0030", bd=0, highlightthickness=0, padx=0, pady=0, command=TrainButton)
btrain.grid(row=0, column=0, sticky="nsew", padx=0, pady=10)

#compare button
compimg = PhotoImage(file=comppath)
bcompare = Button(buttonframe, image=compimg, bg="#1c0030", activebackground="#1c0030", bd=0, highlightthickness=0, padx=0, pady=0, command=CompareButton)
bcompare.grid(row=0,column=1, sticky="nsew", padx=0, pady=10)

root.mainloop()