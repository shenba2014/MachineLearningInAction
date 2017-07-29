from numpy import *


def loadDataSet(fileName):
    numFeature = len(open(fileName).readline().split("\t")) - 1
    dataMatrix = []
    labelMatrix = []
    file = open(fileName)
    for line in file.readlines():
        lineArray = []
        currentLine = line.strip().split("\t")
        for i in range(numFeature):
            lineArray.append(float(currentLine[i]))
        dataMatrix.append(lineArray)
        labelMatrix.append(float(currentLine[-1]))
    return dataMatrix, labelMatrix


def standRegres(xArray, yArray):
    xMattrix = mat(xArray)
    yMattrix = mat(yArray).T
    xTx = xMattrix.T * xMattrix
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMattrix.T * yMattrix)
    return ws


def lwlr(testPoint, xArray, yArray, k=1.0):
    xMattrix = mat(xArray)
    yMattrix = mat(yArray).T
    m = shape(xMattrix)[0]
    weights = mat(eye((m)))
    for j in range(m):
        diffMat = testPoint - xMattrix[j, :]
        weights[j, j] = exp(diffMat * diffMat.T / (-2.0 * k**2))
    xTx = xMattrix.T * (weights * xMattrix)
    if linalg.det(xTx) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = xTx.I * (xMattrix.T * (weights * yMattrix))
    return testPoint * ws


def lwlrTest(testArray, xArray, yArray, k=1.0):
    m = shape(testArray)[0]
    yHat = zeros(m)
    for i in range(m):
        yHat[i] = lwlr(testArray[i], xArray, yArray, k)
    return yHat


def rssError(yArray, yHatArray):
    return ((yArray - yHatArray)**2).sum()


def ridgeRegress(xMattrix, yMattrix, lam=0.2):
    xTx = xMattrix.T * xMattrix
    denom = xTx + eye(shape(xMattrix)[1]) * lam
    if linalg.det(denom) == 0.0:
        print "This matrix is singular, cannot do inverse"
        return
    ws = denom.I * (xMattrix.T * yMattrix)
    return ws


def ridgeTest(xArray, yArray):
    xMattrix = mat(xArray)
    yMattrix = mat(yArray).T
    yMean = mean(yMattrix, 0)
    yMattrix = yMattrix - yMean
    xMean = mean(xMattrix, 0)
    xVar = var(xMattrix, 0)
    xMattrix = (xMattrix - xMean) / xVar
    numTests = 30
    wMat = zeros((numTests, shape(xMattrix)[1]))
    for i in range(numTests):
        ws = ridgeRegress(xMattrix, yMattrix, exp(i - 10))
        wMat[i, :] = ws.T
    return wMat


def stageWise(xArray, yArray, eps=0.01, numIt=300):
    xMattrix = mat(xArray)
    yMattrix = mat(yArray).T
    yMean = mean(yMattrix, 0)
    yMattrix = yMattrix - yMean
    xMattrix = regularize(xMattrix)
    m, n = shape(xMattrix)
    returnMattrix = zeros(numIt, n)
    ws = zeros((n, 1))
    wsTests = ws.copy()
    wsMax = ws.copy()
    for i in range(numIt):
        print ws.T
        lowestError = inf
        for j in range(n):
            for sign in [-1, 1]:
                wsTest = ws.copy()
                wsTest[j] += eps * sign
                yTest = xMattrix * wsTest
                rssE = rssError(yMattrix.A, yTest.A)
                if rssE < lowestError:
                    lowestError = rssE
                    wsMax = wsTest
            ws = wsMax.copy()
            returnMattrix[i, :] = ws.T
    return returnMattrix
