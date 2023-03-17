import numpy as np
from autograd import grad
import matplotlib.pyplot as plt
from cec2017.functions import f1,f2, f3,f5

def booth(x):
    return (x[0]+2*x[1]-7)**2+(2*x[0]+x[1]-5)**2

MAX_X = 100
PLOT_STEP = 0.1

x_arr = np.arange(-MAX_X, MAX_X, PLOT_STEP)
y_arr = np.arange(-MAX_X, MAX_X, PLOT_STEP)
X, Y = np.meshgrid(x_arr, y_arr)
Z = np.empty(X.shape)

wsp=0.000001
DIMENSIONALITY = 10
x = np.random.uniform(-MAX_X, MAX_X, size=DIMENSIONALITY)
q = f1
dq = grad(q)

for i in range(X.shape[0]):
    for j in range(X.shape[1]):
        Z[i, j] = q(np.array([X[i, j], Y[i, j]]))

plt.contour(X, Y, Z, 20)

for i in range (100):
    d=dq(x)
    xtemp=x
    x=x-wsp*d
    print([i, x, q(x), d])
    plt.arrow(xtemp[0], xtemp[1], x[0]-xtemp[0], x[1]-xtemp[1], head_width=1, head_length=1, fc='k', ec='k')


print(f"x={x} q(x)={q(x)}")

plt.show()

