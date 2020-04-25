def WHK(d):
    T = len(d)
    S = [T, T+1]
    t = T
    s = [0]*(T-1) + [T+1]
    Z = [0]*(T-1)+[K+h*d[T-1]]+[0]
    t -= 1
    while t > 0:
        # k is subset of S
        for index, k in enumerate(S):
            if k <= s[t]:
                if k <= T:
                    l = S[index+1]
                    if (Z[k-1]-Z[l-1])/sum(d[k-1:l-1]) < (T-t+1)*h:
                        s[t-1] = k
                        k_value = k
                        break
                else:
                    l = T+1
                    s[t-1] = l
                    break
        Z[t-1] = K + (T-t+1)*h*sum(d[t-1:s[t-1]-1]) + Z[s[t-1]-1]
        if t==1:
            ind = S.index(s[t-1])
            S = [1] + S[ind:]
        else:
            tr = 0
            for t_r in S:
                if t_r <= s[t]:
                    t_rplus1 = S[S.index(t_r)+1]
                    if (Z[t-1]-Z[t_r-1])/sum(d[t-1:t_r-1]) > (Z[t_r-1]-Z[t_rplus1-1])/sum(d[t_r-1:t_rplus1-1]):
                        tr = t_r
                        break
            if tr == 0:
                S = [t] + S
            else:
                t_r_ind = S.index(t_r)
                S = [t] + S[t_r_ind:]
        t -= 1
    t = 1
    z = [0]*T
    while t <= T:
        z[t-1] = sum(d[t-1:s[t-1]-1]) 
        t = s[t-1]
    print(f'G(i) = {Z}')
    print(f'x_t = {z}')


if __name__ == "__main__":
    K, h, d = 100, 1, [10, 60, 15, 150, 110]
    # K, h, d = 300, 1, [40, 70, 90, 50, 30, 100]
    WHK(d)


