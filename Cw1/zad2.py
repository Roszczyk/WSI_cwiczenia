import numpy as np

w = np.array([8, 3, 5, 2]) #waga przedmiotów
W = 9 #maksymalna waga plecaka
p = np.array([16, 8, 9, 6]) #wartość przedmiotów
ppw=p/w 

def checkCurrent(current):
    currentP=0
    currentW=0
    possibleP=0
    for i in range(len(current)):
        if(current[i]==1):
            currentW=currentW+w.item(i)
            currentP=currentP+p.item(i)
        if(currentW>W):
            currentP=0
            break
    if(currentW<W):
        rest=w.size-len(current)
        sorted_items=[]
        best_ppw=0
        for j in range(rest):
            for i in range(rest):
                if (ppw.item(w.size-rest+i) > best_ppw):
                    best_ppw = ppw.item(w.size-rest+i)
                    best_thing=w.size-rest+i
            sorted_items.append(best_thing)
            ppw[best_thing]=0
            best_ppw=0
        restW=W-currentW
        count=0
        while(restW>0):
            restW=restW-w.item(sorted_items[count])
            possibleP=possibleP+p.item(sorted_items[count])
            if(restW>0):
                count=count+1
        possibleP=possibleP-((0-restW)/w.item(sorted_items[count]))*p.item(sorted_items[count])
    return possibleP

print(checkCurrent([0,1]))
    
    
