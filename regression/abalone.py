import regression
from numpy import *

xArray, yArray = regression.loadDataSet("./regression/abalone.txt")

# yHat01 = regression.lwlrTest(xArray[100:199], xArray[0:99], yArray[0:99], 0.1)
# yHat1 = regression.lwlrTest(xArray[100:199], xArray[0:99], yArray[0:99], 1)
# yHat10 = regression.lwlrTest(xArray[100:199], xArray[0:99], yArray[0:99], 10)

# print regression.rssError(yArray[100:199], yHat01)
# print regression.rssError(yArray[100:199], yHat1)
# print regression.rssError(yArray[100:199], yHat10)

# wsStand = regression.standRegres(xArray[0:99], yArray[0:99])
# yHat = mat(xArray[100:199]) * wsStand
# print regression.rssError(yArray[100:199], yHat.T.A)

# ridgeWeights = regression.ridgeTest(xArray, yArray)

# import matplotlib.pyplot as plt
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(ridgeWeights)
# plt.show()
print regression.stageWise(xArray, yArray, 0.01, 200)