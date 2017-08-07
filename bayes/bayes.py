from numpy import *
# from math import *

def loadDataSet():
    postingList=[['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                 ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                 ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him'],
                 ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                 ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                 ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive, 0 not
    return postingList,classVec

def createVocabList(dataSet):
    vocabList = set([])
    for document in dataSet:
        vocabList = vocabList | set(document)
    return list(vocabList)

def setOfWordsToVec(vocabList, inputDocument):
    wordsVec = [0] * len(vocabList)
    for word in inputDocument:
        if word in vocabList:
            wordsVec[vocabList.index(word)] = 1
        else:
            print "The word %s is not in my vocabulary" % word
    return wordsVec

def bagOfWordsToVec(vocabList, inputDocument):
    wordsVec = [0] * len(vocabList)
    for word in inputDocument:
        if word in vocabList:
            wordsVec[vocabList.index(word)] +=1
        else:
            print "The word %s is not in my vocabulary" % word
    return wordsVec

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords)
    p1Num = ones(numWords)
    p0Denom = 2.0
    p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])

    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p0 = sum(vec2Classify * p0Vec) + log(pClass1)
    p1 = sum(vec2Classify * p1Vec) + log(1 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def testingNB():
    dataSet, classVec = loadDataSet()
    vocabList = createVocabList(dataSet)

    # print vocabList

    trainMatrix = []
    for document in dataSet:
        trainMatrix.append(setOfWordsToVec(vocabList, document))

    p0v,p1v,pAb = trainNB0(trainMatrix, classVec)
    # print pAb
    # print p0v
    # print p1v

    testEntry = ['love', 'my', 'dalmation']
    testVec = setOfWordsToVec(vocabList, testEntry)
    print classifyNB(testVec, p0v, p1v, pAb)

    testEntry = ['stupid', 'garbage']
    testVec = setOfWordsToVec(vocabList, testEntry)
    print classifyNB(testVec, p0v, p1v, pAb)

# testingNB()
def textParse(bigString):
    import re
    tokens = re.split(r'\\w*', bigString)
    return [tok.lower() for tok in tokens if len(tok) > 2]

def spamTest():
    docList = []
    classList = []
    fullText = []
    for i in range(1, 26):
        wordList = textParse(open("./bayes/email/spam/%d.txt" % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open("./bayes/email/ham/%d.txt" % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50)
    testSet = []
    for i in range(10):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainingMattrix = []
    trainingClasses = []
    for docIndex in trainingSet:
        trainingMattrix.append(setOfWordsToVec(vocabList, docList[docIndex]))
        trainingClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainingMattrix), array(trainingClasses))
    errorCount = 0
    for testDocIndex in testSet:
        testVec = setOfWordsToVec(vocabList, docList[testDocIndex])
        forcastedClass = classifyNB(array(testVec), p0V, p1V, pSpam)
        if forcastedClass != classList[testDocIndex]:
            errorCount += 1 
    print "the error rate is:", float(errorCount) / len(testSet)

if __name__ == "__main__":
    testingNB()