from numpy import *
import operator


def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    #create a repeat array(N,1) with the provided value
    #subtract the orginal dataSet
    diffMat = tile(inX, (dataSetSize, 1)) - dataSet
    # print tile(inX,(dataSetSize, 1))
    # print diffMat

    #power 2
    sqDiffMat = diffMat**2
    #get the sum of all powers
    sqDistances = sqDiffMat.sum(axis=1)
    # print sqDistances

    #extract
    distances = sqDistances**0.5
    # print distances

    #just return the index not the data
    sortedDistIndicies = distances.argsort()
    # print sortedDistIndicies

    classCount = {}

    for i in range(k):
        voteILabel = labels[sortedDistIndicies[i]]
        classCount[voteILabel] = classCount.get(voteILabel, 0) + 1

    #print classCount

    sorttedClassCount = sorted(
        classCount.iteritems(), key=operator.itemgetter(1), reverse=True)

    #print sorttedClassCount

    return sorttedClassCount[0][0]
