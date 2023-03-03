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
for i in range(len(ppw)):
    if ppw[i] > best_ppw:
        best_ppw = ppw[i]
        best_thing = i

