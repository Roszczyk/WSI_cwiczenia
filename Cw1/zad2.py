import cec2017
import numpy as np
from cec2017.functions import f1
from autograd import grad

def booth(x):
    return ((x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2)

stop=0
wsp=0.1

UPPER_BOUND = 100
DIMENSIONALITY = 2
#wylosuj punkt x:
x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY)

q = booth
dq = grad(q)
d=dq(x)

print(f"x={x} q(x)={q(x)} gradient: {d}")

# #wyznacz ocenę x
# print(x)
# print(x.shape)
# print('q(x) = %.6f' %q)
