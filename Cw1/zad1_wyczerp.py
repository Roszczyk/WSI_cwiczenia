import numpy as np
import time
start = time.time()

w = np.array([8, 3, 5, 2]) #waga przedmiotów
W = 9 #maksymalna waga plecaka
p = np.array([16, 8, 9, 6]) #wartość przedmiotów

optionP=[]

for i in range(2**w.size):
    currentW = 0
    currentP=0
    x=bin(i).lstrip("0b").zfill(w.size)
    for j in range(w.size):
        if(x[j]=="1"):
            currentW=currentW+w.item(j)
            currentP=currentP+p.item(j)
    if(currentW>W):
        currentP=0
    optionP.append(currentP)

best_score=0
for i in range(len(optionP)):
    if optionP[i] > best_score:
        best_score = optionP[i]
        best_option = i

print(f"option {bin(best_option).lstrip('0b').zfill(4)} with score {best_score}")

end = time.time()
total = end - start
print("{0:02f}s".format(total))