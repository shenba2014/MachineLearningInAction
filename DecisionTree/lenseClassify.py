from trees import createTree
from treePlotter import createPlot

file = open("./DecisionTree/lenses.txt")
lenses =[line.strip().split("\t") for line in file.readlines()]
lenseLabels = ["age", "prescript", "astigmatic", "tearRate"]
tree = createTree(lenses, lenseLabels)
print tree
createPlot(tree)