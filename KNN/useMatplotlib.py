import matplotlib
import matplotlib.pyplot as plt
from datingSample import datingDataToMatrix
from numpy import array

dataMatrix, labels = datingDataToMatrix("./KNN/datingTestSet.txt")

fig = plt.figure()
ax = fig.add_subplot(111)
# ax.scatter(dataMatrix[:, 1], dataMatrix[:, 2])
# only show the second and third column
# with color setting
ax.scatter(dataMatrix[:, 1], dataMatrix[:, 2], c=[446] * len(labels))

# print [15] * len(labels)
plt.show()


