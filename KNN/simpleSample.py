from kNN import classify0
from numpy import array


def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


if __name__ == "__main__":
    dataSet, labels = createDataSet()
    print classify0([0, 0.1], dataSet, labels, 3)
