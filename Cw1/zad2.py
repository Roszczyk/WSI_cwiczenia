import cec2017
import numpy as np
from cec2017.functions import f1
from autograd import grad


UPPER_BOUND = 100
DIMENSIONALITY = 2
#wylosuj punkt x:
x = np.random.uniform(-UPPER_BOUND, UPPER_BOUND, size=DIMENSIONALITY)

#wyznacz ocenę x
print(x)
q = f1
print(f"x={x}")
print('q(x) = %.6f' %q(x))

grad_fct = np.gradient(q)
print(f"gradient: {grad_fct}")
# gradinet = grad_fct(x)
# print(gradinet)