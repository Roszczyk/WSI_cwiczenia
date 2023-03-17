import numpy as np
from cec2017.functions import f1,f4, f5

MU=20
MUTATION_PROBABILITY=np.random.uniform(0, 1, 1)[0]

UPPER_BOUND = 100
DIMENSIONALITY = 10

x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY)

#wyznacz ocenę x
print(x)

q = f1(x)

print(q)