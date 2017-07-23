from numpy import *


def loadDataSet(fileName):
    dataMatrix = []
    labelMatrix = []
    file = open(fileName, 'r')
    lines = file.readlines()
    for line in lines:
        lineArray = line.strip().split('\t')
        dataMatrix.append([float(lineArray[0]), float(lineArray[1])])
        labelMatrix.append(float(lineArray[2]))
    return dataMatrix, labelMatrix


def selectJrand(i, m):
    j = i
    while (j == i):
        j = int(random.uniform(0, m))
    return j


def clipAlpha(aj, L, H):
    if (aj < L):
        a = L
    if (aj > H):
        a = H
    return aj

if __name__ == "__main__":
    dataMatrix, labelMatrix = loadDataSet("./SVM/testSet.txt")

    print mat(labelMatrix).shape
