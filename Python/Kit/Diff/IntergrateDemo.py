from sympy import *

x = symbols('x')
y = 3*x+2

def f(x): return 2*x

# integrate(y, (x, 1, oo))

if __name__ == "__main__":
    print(integrate(f(x), (x, 5, 6)))
