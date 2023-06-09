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

def findClass(data):
    for i in range(len(data)):
        if data[i].forward[0]=='none':
            return data[i]

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

def recurrentBayes(node):
    if node.behind[0]=='none':
        value=np.random.choice([True, False], p=[node.true[0], node.false[0]])
        return value
    else:
        values=[]
        for i in range(len(node.behind)):
            values.append(recurrentBayes(findNode(node.behind[i], nodes)))
        valueIndex=[]
        for i in range(2**len(values)):
            valueIndex.append(i)
        for i in range(len(values)):
            if values[i]==True:
                for j in range(int(len(valueIndex)/2)):
                    valueIndex.pop(int(len(valueIndex)/2)-1)
            if values[i]==False:
                for j in range(int(len(valueIndex)/2)):
                    valueIndex.pop(0)
        value=np.random.choice([True, False], p=[node.true[valueIndex[0]], node.false[valueIndex[0]]])
        return value

data, amount = initFile("data.txt")
headlines=data.pop(0)
nodes=[]
for i in range(len(data)):
    nodes.append(Atribute(data[i]))

for i in range(amount):
    dataline=[]
    recurrentBayes(findClass(nodes))

print(recurrentBayes(findClass(nodes)))

savefile=open(os.path.join(sys.path[0], "dataforID3.txt"), "w")


    