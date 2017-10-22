from numpy import *


def loadDataSet(fileName):
    dataSet = []
    file = open(fileName, 'r')
    for line in file.readlines():
        items = line.strip().split('\t')
        floatItems = map(float, items)
        dataSet.append(floatItems)
    return dataSet


def distEclud(vecA, vecB):
    return sqrt(sum(power(vecA - vecB, 2)))


def randCend(dataSet, k):
    n = shape(dataSet)[1]
    cendriods = mat(zeros((k, n)))
    for j in range(n):
        minJ = min(dataSet[:, j])
        rangeJ = float(max(dataSet[:, j]) - minJ)
        cendriods[:, j] = minJ + rangeJ * random.rand(k, 1)
    return cendriods


def kMeans(dataSet, k, distMeans=distEclud, createCend=randCend):
    m = shape(dataSet)[0]
    print m
    clusterAssignment = mat(zeros((m, 2)))
    randCends = createCend(dataSet, k)
    clusterChanged = True
    while clusterChanged:
        clusterChanged = False
        for i in range(m):
            minDistance = inf
            minJ = -1
            for j in range(k):
                distance = distMeans(dataSet[i, :], randCends[j, :])
                if (distance < minDistance):
                    minDistance = distance
                    minJ = j
            if (clusterAssignment[i, 0] != minJ):
                clusterChanged = True
            clusterAssignment[i, :] = minJ, distance**2
        print randCends
        for cent in range(k):
            pstInCluster = dataSet[nonzero(clusterAssignment[:, 0].A == cent)[
                0]]
            randCends[cent, :] = mean(pstInCluster, axis=0)

    return randCends, clusterAssignment


def biKmeans(dataSet, k, distMeas=distEclud):
    m = shape(dataSet)[0]
    clusterAssignment = mat(zeros((m, 2)))
    cendriod0 = mean(dataSet, axis=0).tolist()[0]
    # print mean(dataSet, axis = 0).tolist()
    centList = [cendriod0]
    for j in range(m):
        clusterAssignment[j, 1] = distMeas(mat(cendriod0), dataSet[j, :])**2
        # print clusterAssignment[j,1]
    # print clusterAssignment[:,0].A
    # print nonzero(clusterAssignment[:,0].A == 0)[0]
    while (len(centList) < k):
        lowestSSE = inf
        for i in range(len(centList)):
            ptsInCurrCluster = dataSet[nonzero(clusterAssignment[:, 0].A == i)[
                0], :]
            cendroidMat, splitClusAss = kMeans(ptsInCurrCluster, 2, distMeas)
            sseSplit = sum(splitClusAss[:, 1])
            sseNoSplit = sum(clusterAssignment[nonzero(
                clusterAssignment[:, 0].A != i)[0], 1])
            print 'sseSplit, sseNoSplit:', sseSplit, sseNoSplit
            if (sseNoSplit + sseSplit) < lowestSSE:
                bestCentToSplit = i
                bestNewCent = cendroidMat
                bestClusAss = splitClusAss.copy()
                lowestSSE = sseNoSplit + sseSplit
        bestClusAss[nonzero(bestClusAss[:, 0].A == 1)[0], 0] = len(centList)
        bestClusAss[nonzero(bestClusAss[:, 0].A == 0)[0], 0] = bestCentToSplit
        print 'the bestCentToSplit is: ', bestCentToSplit
        print 'the len of bestClustAss is: ', len(bestClusAss)
        centList[bestCentToSplit] = bestNewCent[0, :].tolist()[
            0]  #replace a centroid with two best centroids
        centList.append(bestNewCent[1, :].tolist()[0])
        clusterAssignment[nonzero(clusterAssignment[:, 0].A == bestCentToSplit)[
            0], :] = bestClusAss  #reassign new clusters, and SSE
    return mat(centList), clusterAssignment


if __name__ == "__main__":
    dataSetMatrix = mat(loadDataSet('./kMeans/testSet2.txt'))
    # print min(dataSetMatrix[:, 0])
    # print max(dataSetMatrix[:, 0])
    # print min(dataSetMatrix[:, 1])
    # print max(dataSetMatrix[:, 1])
    # randCends, clusterAssignment = kMeans(dataSetMatrix, 4)
    # print randCends
    # print 'assignment'
    # print clusterAssignment
    biKmeans(dataSetMatrix, 10)
