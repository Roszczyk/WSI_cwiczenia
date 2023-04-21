import os
import sys
import numpy as np

class BreastCancerData:
    def __init__(self, array):
        self.Class=array[0]
        self.age=array[1]
        self.menopause=array[2]
        self.tumor_size=array[3]
        self.inv_nodes=array[4]
        self.node_caps=array[5]
        self.deg_malig=array[6]
        self.breast=array[7]
        self.breast_quad=array[8]
        self.irradiat=array[9]

def initFile():
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
        dataArray.append(BreastCancerData(line_array))
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

dataArray=initFile()
print(len(dataArray))
dataArray, testingData = divideData(dataArray) 
print(len(dataArray))
print(len(testingData))

for i in range(len(testingData)):
    print(testingData[i].age)