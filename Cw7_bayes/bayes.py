import numpy as np
import os
import sys

class Node:
    def __init__(self, data):
        self.name=data[0][0]
        self.behind=data[1]
        self.true=data[2]
        self.false=data[3]
        self.forward=data[4]


def initFile(fileName): #odczytanie danych z pliku i stworzenie obiektów danych
    path_to_data=os.path.join(sys.path[0], fileName)
    file=open(path_to_data)
    i=0
    dataArray=[]
    file_text=file.read()
    file_lines=file_text.split("\n")
    for i in range(len(file_lines)):
        file_line=file_lines[i]
        line_array=file_line.split(",")
        for j in range(len(line_array)):
            line_array[j]=line_array[j].split("+")
        dataArray.append(line_array)
    file.close()
    return dataArray



data = initFile("data.txt")
nodes=[]
for i in range(len(data)-1):
    nodes.append(Node(data[i+1]))