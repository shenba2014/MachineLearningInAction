from kNN import classify0
from numpy import *
import os
from autoNorm import autoNorm


def img2Vector(fileName):
    file = open(fileName)
    returnVector = zeros((1, 1024))
    for i in range(32):
        line = file.readline()
        for j in range(32):
            returnVector[0, 32 * i + j] = int(line[j])

    return returnVector


def getTrainingMatrix():
    baseDir = "./KNN/trainingDigits"
    fileList = os.listdir(baseDir)
    fileCount = len(fileList)
    trainingMatrix = zeros((fileCount, 1024))
    labels = []
    for i in range(fileCount):
        fileName = fileList[i]
        trainingMatrix[i:] = img2Vector(baseDir + "/" + fileName)
        labels.append(fileName.split("_")[0])
    return trainingMatrix, labels


def testDigitIdentifier():
    trainingMatrix, labels = getTrainingMatrix()
    # normMatrix, ranges, min = autoNorm(trainingMatrix)

    baseTestFileDir = "./KNN/testDigits"
    testFileList = os.listdir(baseTestFileDir)
    testFileCount = len(testFileList)
    errorCount = 0

    for i in range(testFileCount):
        fileName = testFileList[i]
        expectDigit = fileName.split("_")[0]
        testVector = img2Vector(baseTestFileDir + "/" + fileName)
        actualDigit = classify0(testVector, trainingMatrix,
                                labels, 3)
        if (expectDigit != actualDigit):
            errorCount = errorCount + 1
            print "digit came back from classifier is %s, but expected one is %s" % (
                actualDigit, expectDigit)

    print "error rate is %f" % (errorCount / float(testFileCount))

testDigitIdentifier()
