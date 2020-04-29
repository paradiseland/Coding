from math import floor, ceil

def get_n(n):
    n_ceil = ceil(n)
    n_floor = floor(n)
    if lambd/Q2*(k1/n_floor+k2)+lambd*(c1+c2)+Q2/2*(n_floor*i*c1+i*(c2-c1)) > lambd/Q2*(k1/n_ceil+k2)+lambd*(c1+c2)+Q2/2*(n_ceil*i*c1+i*(c2-c1)):
        n = n_ceil
    else:
        n=n_floor
    return n
 


if __name__ == "__main__":
    lambd = 189*365
    c1 = 30
    c2 = 73
    k1 = 700
    k2 = 120
    i = .3
    n = get_n((k1*(c2-c1)/k2/c1)**.5)
    Q2 = (2*lambd*(k1/n+k2)/(n*i*c1+i*c2-i*c1))**.5
    
    Q1 = Q2*n

    C = (k1/(n*T2)+c1*lambd+(n-1)/2*Q2*i*c1)/365+(lambd/Q2*k2 + lambd*c2+Q2/2*i*c2)/365
    C_ = lambd/Q2*(k1/n+k2)+lambd*(c1+c2)+Q2/2*(n*i*c1+i*(c2-c1))
    print(Q2,Q1,C,C_/365)
