from kNN import classify0
from numpy import *


def datingDataToMatrix(fileName):
    labels = []
    file = open(fileName, 'r')
    lines = file.readlines()
    numberOfLine = len(lines)
    returnMatrix = zeros((numberOfLine, 3))
    index = 0
    for line in lines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMatrix[index] = listFromLine[0:-1]

        label = listFromLine[-1]
        labels.append(label)

        index = index + 1
    return returnMatrix, labels

if __name__ == "__main__":
    returnMatrix, labels = datingDataToMatrix("./KNN/datingTestSet.txt")

    print classify0([6487, 3.540265, 0.822483], returnMatrix, labels, 3)
