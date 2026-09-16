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
