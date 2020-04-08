from sympy import *

x = symbols('x')

y = 2*x**3+3


if __name__ == "__main__":
    print(diff(y, x))
