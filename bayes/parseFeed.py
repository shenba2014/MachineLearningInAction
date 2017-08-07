import feedparser
import bayes
import random


def calMostFeq(vocabList, fullText):
    import operator
    freqDict = {}
    for token in vocabList:
        freqDict[token] = fullText.count(token)
    sortedFeq = sorted(freqDict, key=operator.itemgetter(1), reverse=True)
    return sortedFeq[:30]


def localWord(feed1, feed0):
    docList = []
    classList = []
    fullText = []
    minLength = min(len(feed1['entries']), len(feed0['entries']))
    for i in range(minLength):
        wordList = bayes.textParse(feed1['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = bayes.textParse(feed0['entries'][i]['summary'])
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)

    vocabList = bayes.createVocabList(docList)
    top30words = calMostFeq(vocabList, fullText)
    for pairW in top30words:
        if (pairW[0] in vocabList):
            vocabList.remove(pairW[0])

    trainingSet = range(2 * minLength)
    testSet = []
    for i in range(20):
        randIndex = int(random.uniform(0, len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del (trainingSet[randIndex])

    trainMatrix = []
    trainClass = []

    for docIndex in trainingSet:
        trainMatrix.append(bayes.bagOfWordsToVec(vocabList, docList[docIndex]))
        trainClass.append(classList[docIndex])

    p0V, p1V, pSapm = bayes.trainNB0(trainMatrix, trainClass)

    errorCount = 0

    for docIndex in testSet:
        calculatedClass = bayes.classifyNB(
            bayes.bagOfWordsToVec(vocabList, docList[docIndex]), p0V, p1V,
            pSapm)
        if (calculatedClass != classList[docIndex]):
            errorCount += 1

    print "error rate is: ", float(errorCount) / len(testSet)
    return vocabList, p0V, p1V


def getTopWords():
    import operator
    ny = feedparser.parse("http://newyork.craigslist.org/stp/index.rss")
    sf = feedparser.parse("http://sfbay.craigslist.org/stp/index.rss")
    vocabList, p0V, p1V = localWord(ny, sf)
    topNY = []
    topSF = []
    for i in range(len(p0V)):
        if (p0V[i] > -6.0):
            topNY.append((vocabList[i], p0V[i]))
        if (p1V[i] > -6.0):
            topSF.append((vocabList[i], p1V[i]))

    sortedNY = sorted(topNY, key=lambda pair: pair[1], reverse=True)
    sortedSF = sorted(topSF, key=lambda pair: pair[1], reverse=True)

    print "NYNYNYNYNY"
    for item in sortedNY:
        print item

    print "SFSFSFSFSF"
    for item in sortedSF:
        print item

getTopWords()