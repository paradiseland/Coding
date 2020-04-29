from math import floor, ceil

# n = 4

def get_n(n):
    n_ceil = ceil(n)
    n_floor = floor(n)
    if (k1/(n_floor*T2)+c1*lambd+(n_floor-1)/2*Q2*i*c1)/365 > (k1/(n_ceil*T2)+c1*lambd+(n_ceil-1)/2*Q2*i*c1)/365:
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

    Q2 = (2*k2*lambd/(i*c2))**.5
    T2 = Q2/lambd
    C2 = (lambd/Q2*k2 + lambd*c2+Q2/2*i*c2)/365
    n = get_n((k1*c2/k2/c1)**.5)
    print('n=',n)
    Q1 = n*Q2
    C1 =(k1/(n*T2)+c1*lambd+(n-1)/2*Q2*i*c1)/365
    print('Q2:{:.2f} T2:{} C2:{:.2f}\nQ1:{:.2f} C1:{:.2f}\nC1+C2:{:.2f}'.format(Q2,T2,C2,Q1,C1,C1+C2))
