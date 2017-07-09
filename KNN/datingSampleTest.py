from datingSample import datingDataToMatrix
from kNN import classify0
from autoNorm import autoNorm
from numpy import *


def datingClassTest():
    hoRatio = 0.10
    dataMatrix, labels = datingDataToMatrix("./KNN/datingTestSet.txt")
    normMatrix, ranges, min = autoNorm(dataMatrix)

    rows = normMatrix.shape[0]
    numTestVecs = int(hoRatio * rows)

    errorCount = 0
    for i in range(numTestVecs):
        # index = random.randint(1, rows)
        index = i
        testRow = normMatrix[index, :]
        expectClass = labels[index]
        actualClass = classify0(testRow, normMatrix[numTestVecs:rows, :],
                                labels[numTestVecs:rows], 3)
        if (expectClass != actualClass):
            errorCount = errorCount + 1
            print "the classifier came back with: %s, the real answer is: %s" % (
                expectClass, actualClass)

    print "total error rate is %f" % (errorCount / float(numTestVecs))


datingClassTest()
