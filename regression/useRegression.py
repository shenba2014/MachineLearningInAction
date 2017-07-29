import regression
from numpy import *

xArray, yArray = regression.loadDataSet("./regression/ex0.txt")
# print xArray
# print xArray[0:2]

ws = regression.standRegres(xArray, yArray)

xMattrix = mat(xArray)
yMattrix = mat(yArray)
# yHat = xMattrix * ws

import matplotlib.pylab as plt
fig = plt.figure()
ax = fig.add_subplot(111)
# print len(xMattrix[:, 1].flatten().A[0])
# print len(yHat.T[:,0].flatten().A[0])
# ax.scatter(xMattrix[:, 1].flatten().A[0], yMattrix.T[:, 0].flatten().A[0])
# ax.scatter(xMattrix[:, 1].flatten().A[0], yHat[:, 0].flatten().A[0])

# xCopy = xMattrix.copy()
# xCopy.sort(0)
# yHat = xCopy * ws
# ax.scatter(xCopy[:, 1], yHat)
# ax.scatter(xCopy[:, 1].flatten().A[0], yHat[:, 0].flatten().A[0])

# plt.show()
# print corrcoef(yHat.T, yMattrix)

# print yArray[0]
# print regression.lwlr(xArray[0], xArray, yArray, 1.0)
# print regression.lwlr(xArray[0], xArray, yArray, 0.01)

xMattrix = mat(xArray)
srtInd = xMattrix[:, 1].argsort(0)
xSort = xMattrix[srtInd][:, 0, :]
yHat = regression.lwlrTest(xArray, xArray, yArray, 0.01)
ax.plot(xSort[:, 1], yHat[srtInd])
ax.scatter(xMattrix[:, 1].flatten().A[0], yMattrix.T[:, 0].flatten().A[0])
plt.show()