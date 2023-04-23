import os
import sys
import numpy as np


def initFile(): #odczytanie danych z pliku i stworzenie obiektów danych
    path_to_data=os.path.join(sys.path[0], "breast-cancer.data")
    file=open(path_to_data)
    i=0
    dataArray=[]
    # dataArrayNames=['class', 'age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad', 'irradiat' ]
    file_text=file.read()
    file_lines=file_text.split("\n")
    for i in range(len(file_lines)-1):
        file_line=file_lines[i]
        line_array=file_line.split(",")
        dataArray.append(line_array)
    file.close()
    return dataArray

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

###     SPRAWDZANIE LICZNOŚCI:  ###

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

def checkEntropy(array, checking): 
    dividedArray=divideByChecked(array, checking)
    count=[]
    entropy=0
    for i in range(len(dividedArray)):
        dividedByClassValue=divideByChecked(array,0)
        for j in range(len(dividedByClassValue)):
            count.append(len(dividedByClassValue[j]))
        


        


###     BUDOWANIE DRZEWA:       ###

def divideByIrradiat(array):
    dataIrradiat=[]
    dataNonIrradiat=[]
    dataUnknownIrradiat=[]
    dividedData=[]
    for i in range(len(array)):
        if(array[i].irradiat=="yes"):
            dataIrradiat.append(array[i])
        if(array[i].irradiat=="no"):
            dataNonIrradiat.append(array[i])
        else:
            dataUnknownIrradiat.append(array[i])
    dividedData.append(dataIrradiat)
    dividedData.append(dataNonIrradiat)
    dividedData.append(dataUnknownIrradiat)
    return dividedData
    

dataArray, testingData = divideData(initFile()) 

