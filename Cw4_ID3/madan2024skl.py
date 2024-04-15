from sklearn.tree import DecisionTreeClassifier, export_graphviz
from library import initFile, divideData, make_data_sklearnable
import numpy as np

def count_accuracy(tree, data):
    classes = []
    for i in data:
        classes.append(i.pop(0))
    attr = data
    return tree.score(attr, classes)

if __name__ == "__main__":
    data = initFile("breast-cancer.data")
    data = make_data_sklearnable(data)
    data, test_data = divideData(data)

    classes = []
    for i in data:
        classes.append(i.pop(0))
    attr = data

    tree = DecisionTreeClassifier(criterion="entropy")
    tree.fit(attr, classes)

    print(f"Accuracy: {round(count_accuracy(tree, test_data)*100)}%")

    