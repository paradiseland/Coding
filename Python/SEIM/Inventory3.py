def main():
    k = 1
    i = 1
    n = len(K)
    N = [[] for i in range(n)]
    N[0].append(1)

    while i <= n:
        i += 1
        if i > n:
            break
        Sigma = sum([K[kk-1] for kk in N[k-1]])/sum([g[kk-1] for kk in N[k-1]])
        if  Sigma <= K[i-1]/g[i-1]:
            k += 1
            N[k-1] = [i]
            continue
        else:
            N[k-1] = list(set(N[k-1]) | set([i]))
            if k > 1:
                l = k
                while l > 1:
                    Sigma_1 = sum([K[kk-1] for kk in N[l-2]])/sum([g[kk-1] for kk in N[l-2]])
                    Sigma_2 = sum([K[kk-1] for kk in N[l-1]])/sum([g[kk-1] for kk in N[l-1]])
                    if Sigma_1 <= Sigma_2:
                        k = l
                        break
                    else:
                        N[l-2] = list(set(N[l-2]) | set(N[l-1]))
                        l -= 1
                if l <= 1:
                    k = l
                    continue

    return k, N[:k]


def get_po2(k, G):
    res = []
    for i in G:
        T = (sum([K[j-1] for j in i])/sum([g[m-1] for m in i]))**.5
        l = 1
        while 2**l < T/(2**.5*T_L):
            l += 1
        
        res.append((l, 2**l*T_L))

    return res


if __name__ == '__main__':
    T_L = 1/52
    lambd = 100000
    K = [700, 425, 260, 500]
    h = [2, 1.75, 1.5, 1]+[0]
    h_ = []
    g = []
    for ind, k in enumerate(h[:len(h)-1]):
        h_.append(h[ind]-h[ind+1])
        g.append(h_[ind]*lambd/2)
    k, N_ = main()
    print('k={}\nG={}'.format(k,N_))
    res = get_po2(k, N_)
    for i in res:
        print('l={}weeks ={:.3f}years'.format(i[0], i[1]))

