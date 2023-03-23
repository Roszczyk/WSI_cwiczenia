import numpy as np
from cec2017.functions import f4, f5


#STAŁE DLA WYWOŁANIA:
BUDGET=10000            #dotępny budżet ewaluacji funkcji celu
MU=10                   #liczba osobników w populacji
tmax=BUDGET/MU          #liczba iteracji
        #MUTATION_PROBABILITY=np.random.uniform(0, 1, 1)[0]  #prawdopodobieństwo mutacji
MUTATION_FORCE=5        #siła mutacji
UPPER_BOUND = 100       #ograniczenie kostkowe
DIMENSIONALITY = 10     #wymiarowość
TOURNAMENT_GROUP=2      #rozmiar grupy w selekcji turniejowej
ELITE=3                 #rozmiar elity w sukcesji elitarnej

#DEKLARACJE ZMIENNYCH
currentPop=[]           #populacja
objFunPop=[]            #wartości funkcji celu dla osobnikow populacji
rankPop=[None]*MU       #ranga dla każdego z osobników populacji
tournamentProb=[]       #wartości prawdopodobieństwa udziału w turnieju dla osobników populacji

#DEFINICJA OPTYMALIZOWANEJ FUNKCJI:
q=f4

#LOSOWANIE POPULACJI POCZĄTKOWEJ:
for i in range(MU):
    currentPop.append(np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY))
    objFunPop.append(q(currentPop[i]))

#NADANIE RANG:
tempFunPop=np.array(objFunPop)
biggest=tempFunPop.max()+1
for i in range(MU):
    curBest=tempFunPop.argmin()
    rankPop[curBest]=i+1
    tempFunPop[curBest]=biggest

#PRAWDOPODOBIEŃSTWO WYBRANIA DO TURNIEJU:
for i in range(MU):
    tournamentProb.append((1/(MU**TOURNAMENT_GROUP))*((MU-rankPop[i]+1)**TOURNAMENT_GROUP-(MU-rankPop[i])**TOURNAMENT_GROUP))

#WYBÓR ELEMENTÓW DO TURNIEJU:
tournament=np.random.choice(MU, TOURNAMENT_GROUP, tournamentProb)
tournamentValues=[]
for i in range(len(tournament)):
    tournamentValues.append(objFunPop[tournament[i]])

#WYBÓR ZWYCIĘZCY TURNIEJU
tournamentWinner=tournament[np.array(tournamentValues).argmin()]

#MUTACJA ZWYCIĘZCY TURNIEJU
print(objFunPop[tournamentWinner])
currentPop[tournamentWinner]=currentPop[tournamentWinner]+MUTATION_FORCE*np.random.normal(0,1)
objFunPop[tournamentWinner]=q(currentPop[tournamentWinner])
print(objFunPop[tournamentWinner])

#SUKCESJA:
# for t in range(tmax):
#     newPop=[]               #deklaracja populacji potomnej
