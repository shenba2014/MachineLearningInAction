import operator
from math import log

from treePlotter import createPlot, getTreeDepth, getTreeLeafCount


def calcShannonEnt(dataSet):
    numEntries = len(dataSet)
    labelCount = {}
    for dataItem in dataSet:
        label = dataItem[-1]
        if label not in labelCount.keys():
            labelCount[label] = 0
        labelCount[label] += 1
    shannonEnt = 0.0
    for key in labelCount.keys():
        prob = float(labelCount[key]) / numEntries
        shannonEnt -= prob * log(prob, 2)
    return shannonEnt


def createDataSet():
    dataSet = [[1, 1, 'yes'], [1, 1, 'yes'], [1, 0, 'no'], [0, 1, 'no'],
               [0, 1, 'no']]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels


def splitDataSet(dataSet, axis, value):
    returnDataSet = []
    for dataItem in dataSet:
        if (dataItem[axis] == value):
            reducedFeatVec = dataItem[:axis]
            reducedFeatVec.extend(dataItem[axis + 1:])
            returnDataSet.append(reducedFeatVec)
    return returnDataSet


def chooseBestFeaturToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEnt(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet) / float(len(dataSet))
            newEntropy += prob * calcShannonEnt(subDataSet)
        infoGain = baseEntropy - newEntropy
        if (infoGain > bestInfoGain):
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature


def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(
        classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]


def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList):
        return classList[0]
    if len(dataSet[0]) == 1:
        return majorityCnt(classList)
    bestFeature = chooseBestFeaturToSplit(dataSet)
    bestFeatureLabel = labels[bestFeature]
    myTree = {bestFeatureLabel: {}}
    del (labels[bestFeature])
    featureValues = [example[bestFeature] for example in dataSet]
    uniqueValues = set(featureValues)
    for value in uniqueValues:
        subLabels = labels[:]
        myTree[bestFeatureLabel][value] = createTree(
            splitDataSet(dataSet, bestFeature, value), subLabels)
    return myTree


def classify(tree, labels, testVal):
    firstKey = tree.keys()[0]
    secondDict = tree[firstKey]
    featIndex = labels.index(firstKey)
    for key in secondDict.keys():
        if testVal[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], labels, testVal)
            else:
                classLabel = secondDict[key]
    return classLabel


def storeTree(tree, fileName):
    import pickle
    file = open(fileName, 'w')
    pickle.dump(tree, file)
    file.close()


def restoreTree(fileName):
    import pickle
    file = open(fileName, 'r')
    return pickle.load(file)

if __name__ == "__main__":
    dataSet, labels = createDataSet()
    print calcShannonEnt(dataSet)
    # bestFeature = chooseBestFeaturToSplit(dataSet)
    # print splitDataSet(dataSet, bestFeature, 1)
    # print splitDataSet(dataSet, bestFeature, 0)
    myTree = createTree(dataSet, labels)
    print myTree
    # createPlot(myTree)
    # print classify(myTree, ['no surfacing', 'flippers'], [1, 1])
    # storeTree(myTree, 'myTree.txt')
