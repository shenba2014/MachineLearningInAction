from datingSample import datingDataToMatrix
from numpy import *

def autoNorm(dataSet):
    min = dataSet.min()
    max = dataSet.max()
    ranges = max - min
    #create empty matrix with same shape
    normDataSet = zeros(dataSet.shape)

    length = dataSet.shape[0]

    # following is normal way(maybe not a professional style)
    # for i in range(length):
    #     for j in range(3):
    #         normDataSet[i][j] = (dataSet[i][j] - min) / ranges

    # following is python style
    normDataSet = dataSet - tile(min, (length, 1))
    normDataSet = normDataSet / tile(ranges, (length, 1))

    return normDataSet,ranges,min 

if __name__ == "__main__":
    dataSet,labels = datingDataToMatrix("./KNN/datingTestSet.txt")
    # print dataSet
    # print 'after normalized'
    normDataSet,ranges,min = autoNorm(dataSet)

    print normDataSet