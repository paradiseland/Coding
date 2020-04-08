from sympy import *

x = symbols("x")
sigma = 25
lambd = 200
h = 3
K = 50
p = 25
mu = 100

def check_table(q): return 1-q*h/(p*lambd)

def l(m): return (x-m)/((2*pi)**.5)*(E**((-x**2)/2))

def nR(lz): return sigma*lz

def Q(nR): return ((2*lambd)*(K+p*nR)/h)**0.5

def L(z): return integrate(l(z), (x, z, oo)).evalf(n=3)


if __name__ == "__main__":
    EOQ = (2*K*lambd/h)**.5
    print("EOQ:", EOQ)
    check = check_table(EOQ) - .5
    z = float(input("check the table {} get z value:".format(str(check))))
    # print("check table value:", check)
    q_0 = EOQ
    q = 0
    while abs(q_0 - q) >2: 
        Lz = L(z)
        nr = nR(Lz)
        q = round(Q(nr))
        print("L(z):",Lz)
        print("n(R):", nr)
        print("Q:", q)
        
        check = check_table(q)-.5
        z = float(input("check the table {} get z value:".format(str(check))))
        print("R:", sigma*z+mu)
        print("q_0&q:", q_0,q)

# EOQ: 81.64965809277261
# check the table 0.45101020514433643 get z value:1.65
# L(z): 0.0206
# n(R): 0.516
# Q: 92
# check the table 0.4448 get z value:1.60
# R: 140.0
# q_0&q: 81.64965809277261 92
# L(z): 0.0232
# n(R): 0.581
# Q: 93
# check the table 0.44420000000000004 get z value:1.59
# R: 139.75
# q_0&q: 81.64965809277261 93
# L(z): 0.0238
# n(R): 0.595
# Q: 93
# check the table 0.44420000000000004 get z value:
