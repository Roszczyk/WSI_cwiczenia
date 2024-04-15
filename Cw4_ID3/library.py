# FUNCTIONS LIBRARY FILE FOR 2024_madan.py
import os
import sys
import numpy as np
import copy


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

def make_data_sklearnable(data):
    from madan2024 import nameValues
    for i in range(len(data[0])):
        attr_names = nameValues(data, i)
        for j in range(len(data)):
            for n in range(len(attr_names)):
                if data[j][i] == attr_names[n]:
                    data[j][i] = n
    return data