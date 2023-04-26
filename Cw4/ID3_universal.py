import os
import sys
import numpy as np


def initFile(fileName): #odczytanie danych z pliku i stworzenie obiektów danych
    path_to_data=os.path.join(sys.path[0], fileName)
    file=open(path_to_data)
    i=0
    dataArray=[]
    file_text=file.read()
    file_lines=file_text.split("\n")
    for i in range(len(file_lines)-1):
        file_line=file_lines[i]
        line_array=file_line.split(",")
        dataArray.append(line_array)
    file.close()
    return dataArray

def log2(value):
    return np.log(value)/np.log(2)

def divideData(data): #podział zbioru danych na dane trenujące i testowe
    trainingData=[]
    testingData=[]
    for i in range(len(data)):
        chooseSet=np.random.choice([0,1],1,p=[0.6,0.4])
        if chooseSet==0:
            trainingData.append(data[i])
        if chooseSet==1:
            testingData.append(data[i])
    return trainingData, testingData

def nameValues(data, checking):      #nazwanie elementów danej kategorii
    unique_list=[]
    for i in range(len(data)):
        if data[i][checking] not in unique_list:
            unique_list.append(data[i][checking])
    return unique_list

def unique(list):
    unique_list = []
    for x in list:
        if x not in unique_list:
            unique_list.append(x)
    return unique_list

def divideByChecked(array, checking):
    partsLists=[]
    valuesList=nameValues(array, checking)
    for i in range(len(valuesList)):
        partsTemp=[]
        for j in range(len(array)):
            if array[j][checking]==valuesList[i]:
                partsTemp.append(array[j])
        partsLists.append(partsTemp)
    return partsLists

def countEntropy(array):
    values=nameValues(array,0)
    count=[]
    for i in range(len(values)):
        countTemp=0
        for j in range(len(array)):
            if array[j][0]==values[i]:
                countTemp=countTemp+1
        count.append(countTemp)
    sumValues=0
    entropy=0
    for i in range(len(count)):
        sumValues=sumValues+count[i]
    for i in range(len(count)):
        prob=count[i]/sumValues
        entropy=entropy-prob*log2(prob)
    return entropy

def checkChildrenEntropy(array, checking): 
    dividedArray=divideByChecked(array, checking)
    entropy=[]
    for i in range(len(dividedArray)):
        entropy.append(countEntropy(dividedArray[i]))
    return entropy

def countInformationGain(parent, parentEntropy, checking):
    ig=parentEntropy
    children=divideByChecked(parent, checking)
    childrenEntropyList=checkChildrenEntropy(parent, checking)
    amount=[]
    for i in range(len(children)):
        amount.append(len(children[i]))
    sum=0
    for i in range(len(amount)):
        sum=sum+amount[i]
    for i in range(len(childrenEntropyList)):
        ig=ig-(amount[i]/sum)*childrenEntropyList[i]
    return ig

def chooseBestPath(dataArray,dataEntropy,columns):
    igList=[]
    for i in range(columns):
        igList.append(countInformationGain(dataArray,dataEntropy,i+1))
    if len(igList)==0:
        bestChoice=None
    else:
        bestChoice=np.array(igList).argmax()+1
    return bestChoice

def recurrentID3(array, array_entropy, columns, depth=0):
    if len(array)==0 or array_entropy == 0:
        return None
    else:
        best_choice = chooseBestPath(array, array_entropy, columns)
        if best_choice==None:
            return None
        child_arrays = divideByChecked(array, best_choice)
        
        for i in range(len(array)):
            array[i].pop(best_choice)
        
        children = []
        for i in range(len(child_arrays)):
            child_entropy = countEntropy(child_arrays[i])
            child = recurrentID3(child_arrays[i], child_entropy, columns - 1, depth + 1)
            children.append(child)

        tree = {
            "attribute": best_choice,
            "children": children
        }
        return tree
    
def predict(data, tree, inputSet):
    if not tree:
        return None
    attribute = tree["attribute"]
    attribute_value = data[attribute - 1]
    if attribute_value not in inputSet[attribute - 1]:
        return None
    index = inputSet[attribute - 1].index(attribute_value)
    subtree = tree["children"][index]
    if not subtree:
        return None
    if "class" in subtree:
        return subtree["class"]
    else:
        return predict(data, subtree, inputSet)



def defineClassSet(data):
    return nameValues(data,0)

def defineInputSet(data):
    inputSet=[]
    for i in range(len(data[0])-1):
        inputSet.append(nameValues(data,i+1))
    return inputSet
        


dataArray, testingData = divideData(initFile("breast-cancer.data"))
columns = len(dataArray[0]) - 1  # liczba kolumn bez klasy

input_set = defineInputSet(dataArray)
tree = recurrentID3(dataArray, countEntropy(dataArray), columns-1)
print(tree)

correct_predictions = 0
for test_data in testingData:
    actual_class = test_data[0]
    predicted_class = predict(test_data, tree, input_set)
    print("actual:    ", actual_class)
    print("predicted: ", predicted_class)
    if actual_class == predicted_class:
        correct_predictions += 1

accuracy = correct_predictions / len(testingData)
print("Accuracy:", accuracy)



