from numpy import *
from adaBoost import loadSimpData


def stumpClassify(dataMatrix, dimen, threshVal,
                  threshIneq):  #just classify the data
    retArray = ones((shape(dataMatrix)[0], 1))
    if threshIneq == 'lt':
        retArray[dataMatrix[:, dimen] <= threshVal] = -1.0
    else:
        retArray[dataMatrix[:, dimen] > threshVal] = -1.0
    return retArray


def buildStump(dataArray, classLabels, D):
    dataMatrix = mat(dataArray)
    labelMatrix = mat(classLabels).T
    m, n = shape(dataMatrix)
    numSteps = 10.0
    bestStump = {}
    bestClassEst = mat(zeros((m, 1)))
    minErro = inf

    for i in range(n):
        rangeMin = dataMatrix[:, i].min()
        rangeMax = dataMatrix[:, i].max()
        stepSize = (rangeMax - rangeMin) / numSteps
        for j in range(-1, int(numSteps) + 1):
            for inequal in ['lt', 'gt']:
                threshVal = (rangeMin + float(j) * stepSize)
                predictedVals = stumpClassify(dataMatrix, i, threshVal,
                                              inequal)
                errArr = mat(ones((m, 1)))
                errArr[predictedVals == labelMatrix] = 0
                weightedError = D.T * errArr
                print "split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" % (
                    i, threshVal, inequal, weightedError)
                if (weightedError < minErro):
                    minErro = weightedError
                    bestClassEst = predictedVals.copy()
                    bestStump['dim'] = i
                    bestStump['thresh'] = threshVal
                    bestStump['ineq'] = inequal
    return bestStump, minErro, bestClassEst


def adaBoostTrainDS(dataArr, classLabels, numIt=40):
    weakClassArray = []
    m = shape(dataArr)[0]
    D = mat(ones((m, 1)) / m)
    aggClassEst = mat(zeros((m, 1)))
    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataArr, classLabels, D)
        print "D:", D.T
        alpha = float(0.5 * log((1.0 - error) / max(error, 1e-16)))
        bestStump['alpha'] = alpha
        weakClassArray.append(bestStump)
        print "classEst:", classEst.T
        expon = multiply(-1 * alpha * mat(classLabels).T, classEst)
        D = multiply(D, exp(expon))
        D = D / D.sum()
        aggClassEst += alpha * classEst
        aggErrors = multiply(
            sign(aggClassEst) != mat(classLabels).T, ones((m, 1)))

        errorRate = aggErrors.sum() / m
        print "total error: ", errorRate
        if errorRate == 0.0:
            break
    return weakClassArray, aggClassEst


dataMatrix, classLabels = loadSimpData()

D = mat(ones((5, 1)) / 5)

# buildStump(dataMatrix, classLabels, D)
classifierArray = adaBoostTrainDS(dataMatrix, classLabels, 9)
