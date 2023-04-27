import os
import sys
import numpy as np
import copy

class Tree:
    def __init__(self, choice,choiceValue, children, Class=None):
        self.choice=choice
        self.choiceValue=choiceValue
        self.children=children
        self.Class=Class

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

def most_frequent(List): #kod skopiowany od GeeksForGeeks
    counter = 0
    num = List[0]
    for i in List:
        curr_frequency = List.count(i)
        if(curr_frequency> counter):
            counter = curr_frequency
            num = i
    return num

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

def recurrentID3(array, arrayEntropy, columns):
    if len(array[0])==1:
        classValues=nameValues(array,0)
        if len(classValues)==1:
            classValue=classValues[0]
        else:
            count=[]
            for i in range(len(array)):
                countTemp=0
                for j in range(len(classValues)):
                    if array[i][0]==classValues[j]:
                        countTemp=countTemp+1
                count.append(countTemp)
            classValue=classValues[np.array(count).argmax()]
        return [Tree(None, None, None, classValue)]
    if len(array[0])>1:
        bestChoice=chooseBestPath(array, arrayEntropy, columns)
        children=divideByChecked(array, bestChoice)
        listOfSubtrees=[]
        for i in range(len(children)):
            tempArray=copy.deepcopy(children[i])
            for j in range(len(tempArray)):
                tempArray[j].pop(bestChoice)
            tree=Tree(bestChoice, children[i][0][bestChoice], recurrentID3(tempArray, countEntropy(tempArray), len(tempArray[0])-1), None)
            listOfSubtrees.append(tree)
        return listOfSubtrees
            
    
def predict(data, tree):
    if tree[0].Class != None:
        print(tree[0].Class)
        return tree[0].Class
    choice=tree[0].choice
    tempArray=copy.deepcopy(data)
    tempArray.pop(choice)
    setOfOptions=[]
    for i in range(len(tree)):
        if tree[i].choiceValue==data[choice]:
            result=predict(tempArray, tree[i].children)
            return result
        setOfOptions.append(tree[i])
    result = predict(tempArray, np.random.choice(setOfOptions, 1)[0].children) #rozwiązanie tymczasowe, bo nie wiem co jest nie tak
    return result



def defineClassSet(data):
    return nameValues(data,0)

def defineInputSet(data):
    inputSet=[]
    for i in range(len(data[0])-1):
        inputSet.append(nameValues(data,i+1))
    return inputSet
        


dataArray, testingData = divideData(initFile("breast-cancer.data"))
columns = len(dataArray[0]) - 1  # liczba kolumn bez klasy

tree=recurrentID3(dataArray, countEntropy(dataArray), len(dataArray[0])-1)

# print(predict(testingData[3], tree))

countTestingData=len(testingData)
countTrue=0

for i in range(countTestingData):
    predicted=predict(testingData[i], tree)
    print(predicted," - ", testingData[i][0])
    if predicted==testingData[i][0]:
        countTrue=countTrue+1

accuracy=countTrue/countTestingData

print("accuracy: ", accuracy)


