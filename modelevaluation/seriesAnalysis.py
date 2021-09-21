import numpy as np

def biggestdifference(x,y):
    if len(x) != len(y):
        print("arrays not the same length")
    return np.argmax(abs(x-y))