import numpy as np
import os
import sys

def findNode(name, list_of_nodes):
    if name=='none':
        return None
    for i in range(len(list_of_nodes)):
        if list_of_nodes[i].name==name:
            return list_of_nodes[i]
    return None

def findInputs(data):
    inputs=[]
    for i in range(len(data)):
        if data[i].behind[0]=='none':
            inputs.append(data[i])
    return inputs

def findClass(data):
    for i in range(len(data)):
        if data[i].forward[0]=='none':
            return data[i]

class Atribute:
    def __init__(self, data):
        self.name=data[0][0]
        self.behind=data[1]
        tempList=[]
        for i in range(len(data[2])):
            tempList.append(float(data[2][i]))
        self.true=tempList
        tempList=[]
        for i in range(len(data[3])):
            tempList.append(float(data[3][i]))
        self.false=tempList
        self.forward=data[4]


class DataLine:
    def __init__(self, input):
        self.input=input

    def generateData(self):
        dataline=[0]
        for i in range(len(self.input)):
            value=np.random.choice([True, False], p=[self.input[i].true[0], self.input[i].false[0]])
            dataline.append(value)
        if self.input[0].forward[0] == self.input[1].forward[0]:
            next=findNode(self.input[0].forward[0], nodes)
            if dataline[1]==True and dataline[2]==True:
                value=np.random.choice([True, False], p=[next.true[0], next.false[0]])
            if dataline[1]==True and dataline[2]==False:
                value=np.random.choice([True, False], p=[next.true[1], next.false[1]])
            if dataline[1]==False and dataline[2]==True:
                value=np.random.choice([True, False], p=[next.true[2], next.false[2]])
            if dataline[1]==False and dataline[2]==False:
                value=np.random.choice([True, False], p=[next.true[3], next.false[3]])   
            dataline.append(value)
        next=findNode(next.forward[0], nodes)
        if dataline[3]==True:
            value=np.random.choice([True, False], p=[next.true[0], next.false[0]])
        if dataline[3]==False:
            value=np.random.choice([True, False], p=[next.true[1], next.false[1]])
        dataline[0]=value
        return dataline



def initFile(fileName): #odczytanie danych z pliku i stworzenie obiektów danych
    path_to_data=os.path.join(sys.path[0], fileName)
    file=open(path_to_data)
    i=0
    dataArray=[]
    file_text=file.read()
    file_lines=file_text.split("\n")
    amount=int(file_lines.pop(0))
    for i in range(len(file_lines)):
        file_line=file_lines[i]
        line_array=file_line.split(",")
        for j in range(len(line_array)):
            line_array[j]=line_array[j].split("+")
        dataArray.append(line_array)
    file.close()
    return dataArray, amount



data, amount = initFile("data.txt")
headlines=data.pop(0)
nodes=[]
for i in range(len(data)):
    nodes.append(Atribute(data[i]))
inputs=findInputs(nodes)


savefile=open(os.path.join(sys.path[0], "dataforID3.txt"), "w")


for i in range(amount):
    dataline=DataLine(inputs).generateData()
    savefile.write(f"{dataline[0]},{dataline[1]},{dataline[2]},{dataline[3]}\n")
    
