import os
import sys
path_to_data=os.path.join(sys.path[0], "breast-cancer.data")
file=open(path_to_data)

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

i=0
dataArray=[]
dataArrayNames=['class', 'age', 'menopause', 'tumor-size', 'inv-nodes', 'node-caps', 'deg-malig', 'breast', 'breast-quad', 'irradiat' ]
file_text=file.read()
file_lines=file_text.split("\n")
for i in range(len(file_lines)-1):
    file_line=file_lines[i]
    line_array=file_line.split(",")
    dataArray.append(BreastCancerData(line_array))

for i in range(len(dataArray)):
    print(dataArray[i].breast)