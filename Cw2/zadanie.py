import numpy as np
from cec2017.functions import f4, f5


#STAŁE DLA WYWOŁANIA:
BUDGET=10000            #dotępny budżet ewaluacji funkcji celu
MU=20                   #liczba osobników w populacji
tmax=BUDGET/MU          #liczba iteracji
MUTATION_PROBABILITY=np.random.uniform(0, 1, 1)[0]  #prawdopodobieństwo mutacji
UPPER_BOUND = 100
DIMENSIONALITY = 10

#DEKLARACJE ZMIENNYCH
t=0                     #dokonana liczba iteracji
currentPop=[]           #populacja
objFunPop=[]            #wartosci funkcji celu dla osobnikow populacji

#DEFINICJA OPTYMALIZOWANEJ FUNKCJI:
q=f4

#LOSOWANIE POPULACJI POCZĄTKOWEJ:
for i in range(MU):
    currentPop.append(np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY))
    objFunPop.append(q(currentPop[i]))
    print(i, currentPop[i], objFunPop[i])