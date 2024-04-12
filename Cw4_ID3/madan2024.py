import os
import sys
import numpy as np
import copy

from library import initFile

METHODS_LIST = ["entropy", "gini"]
CHOSEN_METHOD = METHODS_LIST[0]

class Tree:
    def __init__(self, choice,choiceValue, children, Class=None):
        self.choice=choice              #atrybut, po którym dokonujemy wyboru
        self.choiceValue=choiceValue    #lista klas danego atrybutu
        self.children=children          #poddrzewa
        self.Class=Class                #nie None tylko jeśli to jest liść - wtedy klasa

def log2(value):
    return np.log(value)/np.log(2)

def most_frequent(List): #wskazanie najczęstszego elementu w liście
    counter = 0
    num = List[0]
    for i in set(List):
        curr_frequency = List.count(i)
        if(curr_frequency > counter):
            counter = curr_frequency
            current_best = i
    return current_best

def divideData(data, train_prob = 0.8): #podział zbioru danych na dane trenujące i testowe
    trainingData=[]
    testingData=[]
    for i in range(len(data)):
        chooseSet=np.random.choice([0,1],1,p=[train_prob,1-train_prob])
        if chooseSet==0:
            trainingData.append(data[i])
        if chooseSet==1:
            testingData.append(data[i])
    return trainingData, testingData

def nameValues(data, checking):      #nazwanie klas danego atrybutu
    unique_list=[]
    for i in range(len(data)):
        if data[i][checking] not in unique_list:
            unique_list.append(data[i][checking])
    return unique_list

def divideByChecked(array, checking):   #dzieli dane względem wybranego atrybutu
    partsLists=[]
    valuesList=nameValues(array, checking)
    for i in range(len(valuesList)):
        partsTemp=[]
        for j in range(len(array)):
            if array[j][checking]==valuesList[i]:
                partsTemp.append(array[j])
        partsLists.append(partsTemp)
    return partsLists

def count_entropy_or_gini(array, chosen_method="entropy"):
    if chosen_method == "entropy":
        return countEntropy(array)
    if chosen_method == "gini":
        return countGini(array)

def countEntropy(array):        #liczenie entropii względem danego atrybutu
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

def countGini(array):
    pass

def checkChildrenEntropy(array, checking, chosen_method = "entropy"):      #sprawdzenie entropii względem dzieci
    dividedArray=divideByChecked(array, checking)
    entropy=[]
    for partial_array in dividedArray:
        entropy.append(count_entropy_or_gini(partial_array, chosen_method))
    return entropy

def countInformationGain(parent, parentEntropy, checking, method="entropy"):  #liczenie zysku informacyjnego
    ig=parentEntropy
    children=divideByChecked(parent, checking)
    childrenEntropyList=checkChildrenEntropy(parent, checking, method)
    amount=[]
    for child in children:
        amount.append(len(child))
    sum_amount = sum(amount)
    for i in range(len(childrenEntropyList)):
        ig=ig-(amount[i]/sum_amount)*childrenEntropyList[i]
    return ig

def chooseBestPath(dataArray,dataEntropy,columns,ig_method="entropy"):      #wybieranie najlepszej ścieżki podziału
    igList=[]
    for i in range(columns):
        igList.append(countInformationGain(dataArray,dataEntropy,i+1,ig_method))
    if len(igList)==0:
        bestChoice=None
    else:
        bestChoice=np.array(igList).argmax()+1
    return bestChoice

def recurrentID3(array, arrayEntropy, columns):     #rekurencyjne tworzenie drzewa decyzyjnego 
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
        bestChoice=chooseBestPath(array, arrayEntropy, columns, ig_method=CHOSEN_METHOD)
        children=divideByChecked(array, bestChoice)
        listOfSubtrees=[]
        for i in range(len(children)):
            tempArray=copy.deepcopy(children[i])
            for j in range(len(tempArray)):
                tempArray[j].pop(bestChoice)
            entropy = countEntropy(tempArray)
            tree=Tree(bestChoice, children[i][0][bestChoice], recurrentID3(tempArray, entropy, columns-1), None)
            listOfSubtrees.append(tree)
        return listOfSubtrees
            
    
def predict(data, tree):        # wyliczenie predykcji dla danego wejścia
    if tree[0].Class != None:
        return tree[0].Class
    choice=tree[0].choice
    tempArray=copy.deepcopy(data)
    tempArray.pop(choice)
    setOfOptions=[]
    for subtree in tree:
        if subtree.choiceValue==data[choice]:
            result=predict(tempArray, subtree.children)
            return result
        setOfOptions.append(subtree)
    result = predict(tempArray, np.random.choice(setOfOptions, 1)[0].children)
    return result

def defineClassSet(data):
    return nameValues(data,0)

def accuracy(tree, testData):
    countTrue = 0
    for data in testData:
        predicted=predict(data, tree)
        if predicted==data[0]:
            countTrue=countTrue+1
    return countTrue / len(testData)

def build_tree(dataArray):
    columns = len(dataArray[0]) - 1  # liczba kolumn bez klasy
    tree=recurrentID3(dataArray, count_entropy_or_gini(dataArray, CHOSEN_METHOD), columns)
    return tree

if __name__ == "__main__":
    DATAFILE = "breast-cancer.data"
    # DATAFILE = "agaricus-lepiota.data"
    dataArray, testingData = divideData(initFile(DATAFILE))
    tree = build_tree(dataArray)
    acc = accuracy(tree, testingData)
    print(f"Accuracy = {round(1000*acc)/10}%")