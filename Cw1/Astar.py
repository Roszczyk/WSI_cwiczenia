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
        ppw_temp=np.array(ppw.tolist())
        rest=w.size-len(current)
        sorted_items=[]
        best_ppw=0
        for j in range(rest):
            for i in range(rest):
                if (ppw_temp.item(w.size-rest+i) > best_ppw):
                    best_ppw = ppw_temp.item(w.size-rest+i)
                    best_thing=w.size-rest+i
            sorted_items.append(best_thing)
            ppw_temp[best_thing]=0
            best_ppw=0
        restW=W-currentW
        count=0
        iteration=0
        while(restW>0 and iteration<len(sorted_items)):
            iteration=iteration+1
            restW=restW-w.item(sorted_items[count])
            possibleP=possibleP+p.item(sorted_items[count])
            if(restW>0 and count+1<len(sorted_items)):
                count=count+1
        if(restW<0):
            possibleP=possibleP-((0-restW)/w.item(sorted_items[count]))*p.item(sorted_items[count])
    return possibleP+currentP

def start(x):
    option0=checkCurrent(np.append(x,0).tolist())
    option1=checkCurrent(np.append(x,1).tolist())
    return [option0,option1]

def score(tree,currentBest):
     bestScore=tree[len(tree)-1][currentBest[(len(currentBest)-1)]]
     return bestScore

def buildTree(currentBest, tree):
    startTreeLen=len(tree)
    for i in range(w.size-startTreeLen):
        tree.append(start(currentBest))
        currentBest.append(np.array(tree[startTreeLen+i]).argmax())
    return [currentBest, tree]

currentBest=[]
currentScore=0
tree=[]
result=buildTree(currentBest,tree)
currentBest=result[0]
tree=result[1]
currentScore=score(tree, currentBest)

print(f"Best: {currentBest}, Score: {currentScore}, Tree: {tree}")

print(len(tree))

for i in range(len(tree)):
    print(min(tree[len(tree)-i-1]))
    if(min(tree[len(tree)-i-1])>currentScore):
        tempBest=[]
        temp_tree=[]
        for j in range(len(tree)-i-1):
            tempBest.append(currentBest[j])
            temp_tree.append(tree[j])
        if(currentBest[len(tempBest)]==0):
            tempBest.append(1)
            temp_tree.append(tree[len(tree)-i-1][1])
        else:
            tempBest.append(0)
            temp_tree.append(tree[len(tree)-i-1][0])
        temp_data=buildTree(tempBest, temp_tree)
        temp_Score=score(temp_data[1], temp_data[0])
        if temp_Score>currentScore:
            currentScore=temp_Score
            tree=temp_tree
            currentBest=temp_data[0]
    else:
        continue

print(temp_data[0])
print(currentBest)