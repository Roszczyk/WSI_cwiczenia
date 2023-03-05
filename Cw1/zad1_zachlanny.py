import numpy as np
import time
start = time.time()

w = np.array([8, 3, 5, 2]) #waga przedmiotów
W = 9 #maksymalna waga plecaka
p = np.array([16, 8, 9, 6]) #wartość przedmiotów


ppw=[]
optionP=[]

for i in range(w.size):
    temp_ppw=round(p.item(i)/w.item(i), 2)
    ppw.append(temp_ppw)

best_ppw=0
sorted_items=[]
for j in range(len(ppw)):
    for i in range(len(ppw)):
        if (ppw[i] > best_ppw):
            best_ppw = ppw[i]
            best_thing=i
    sorted_items.append(best_thing)
    ppw[best_thing]=0
    best_ppw=0

currentP=0
currentW=0
solution=[0,0,0,0]
for i in range(len(sorted_items)):
    currentW=currentW+w.item(sorted_items[i])
    if (currentW<W):
        currentP=currentP+p.item(sorted_items[i])
        solution[sorted_items[i]]=1
    else:
        break

print(f"option {solution} with score {currentW}")

end = time.time()
total = end - start
print("{0:02f}s".format(total))