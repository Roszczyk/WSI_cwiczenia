import numpy as np
from cec2017.functions import f4, f5

#STAŁE DLA WYWOŁANIA:
BUDGET=10000            #dotępny budżet ewaluacji funkcji celu
MU=50                  #liczba osobników w populacji
tmax=int(BUDGET/MU)     #liczba iteracji
MUTATION_FORCE=5        #siła mutacji
UPPER_BOUND = 100       #ograniczenie kostkowe
DIMENSIONALITY = 10     #wymiarowość
TOURNAMENT_GROUP=2      #rozmiar grupy w selekcji turniejowej
ELITE=20                 #rozmiar elity w sukcesji elitarnej

for zadanie in range(25):
    #DEKLARACJE ZMIENNYCH
    currentPop=[]           #populacja
    objFunPop=[]            #wartości funkcji celu dla osobnikow populacji
    rankPop=[None]*MU       #ranga dla każdego z osobników populacji
    tournamentProb=[]       #wartości prawdopodobieństwa udziału w turnieju dla osobników populacji

    #DEFINICJA OPTYMALIZOWANEJ FUNKCJI:
    q=f5

    #LOSOWANIE POPULACJI POCZĄTKOWEJ:
    for i in range(MU):
        currentPop.append(np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY))
        objFunPop.append(q(currentPop[i]))


    for t in range(tmax):
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

        #TYMCZASOWE ZMIENNE:
        newPop=[]
        newPopValues=[]

        for i in range(MU):
            #WYBÓR ELEMENTÓW ZA POMOCĄ TURNIEJU:
            tournament=np.random.choice(MU, TOURNAMENT_GROUP, tournamentProb)
            tournamentValues=[]
            for i in range(len(tournament)):
                tournamentValues.append(objFunPop[tournament[i]])

            #WYBÓR ZWYCIĘZCY TURNIEJU
            tournamentWinner=tournament[np.array(tournamentValues).argmin()]

            #MUTACJA ZWYCIĘZCY TURNIEJU
            new=currentPop[tournamentWinner]+MUTATION_FORCE*np.random.normal(0,1,DIMENSIONALITY)
            newPop.append(new)
            newPopValues.append(q(new))

        #DODANIE ELITY DO NOWEJ POPULACJI:
        biggest=np.array(objFunPop).max()+10
        for i in range(ELITE):
            temp=np.array(objFunPop).argmin()
            newPop.append(currentPop[temp])
            newPopValues.append(np.array(objFunPop).min())
            objFunPop[temp]=biggest

        #WYRÓWNYWANIE SKŁADU POPULACJI:
        for i in range(len(newPop)-MU):
            temp=np.array(newPopValues).argmax()
            newPop.pop(temp)
            newPopValues.pop(temp)

        currentPop=newPop
        objFunPop=newPopValues

    print(round(np.array(objFunPop).min(),3))


