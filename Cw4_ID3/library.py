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