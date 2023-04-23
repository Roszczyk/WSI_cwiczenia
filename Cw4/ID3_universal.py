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
        chooseSet=np.random.choice([0,1],1,p=[0.66,0.34])
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
    bestChoice=np.array(igList).argmax()+1
    return bestChoice

def recurrentID3(array,arrayEntropy, iterations, path=[]):
    if countEntropy(array)==0 or iterations==0:
        return path
    bestChoice=chooseBestPath(array, arrayEntropy, iterations)
    arrayChildren=divideByChecked(array,bestChoice)
    path.append(bestChoice)
    arrayChildrenCopy=arrayChildren
    for i in range(len(arrayChildren)):
        for j in range(len(arrayChildrenCopy[i])):
            arrayChildrenCopy[i][j].pop(bestChoice)
    paths=[]
    counts=[]
    for i in range(len(arrayChildrenCopy)):
        tempPath = recurrentID3(arrayChildrenCopy[i],countEntropy(arrayChildrenCopy[i]),iterations-1, path)
        # print(path)
        paths.append(tempPath)
        counts.append(len(tempPath))
        print(counts)
    bestPath=np.array(counts).argmin()
    return paths[bestPath]

        


dataArray, testingData = divideData(initFile("breast-cancer.data")) 
dataEntropy=countEntropy(dataArray)
columns=len(dataArray[0])-1 #liczba kolumn bez klasy
print("Entropy: ", dataEntropy)
bestChoice=chooseBestPath(dataArray,dataEntropy,columns)
print("First: ", bestChoice)
newArray=divideByChecked(dataArray, bestChoice)
print("Len: ", len(newArray))

print(recurrentID3(dataArray, dataEntropy, columns))



