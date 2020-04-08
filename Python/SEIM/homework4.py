from math import sqrt

picks = [1000, 300, 250]
pieces_month = [2000, 1200, 4000]
pieces_case = [200, 6, 10]
volume_case = [2, 7, 1]

f = [i/j*k for i, j, k in zip(pieces_month, pieces_case, volume_case)]
v = [10*sqrt(i)/sum([sqrt(j) for j in f]) for i in f]

# v_i: [0.07226093366316126, 0.6045783467599758, 0.32316071957686293]
restocks = [i/j for i, j in zip(f,v)]
# for i in restocks:
#     print('%.4f'%(i),end =",")
# restocks :27.6775,231.5663,123.7774

# EQS
n = 3

rank = [i/sqrt(j) for i ,j in zip(picks, f)]
# [223.60679774997897, 8.017837257372731, 12.5]

s = 0.1
c_r = 1

sigma_sqrt_fi = sum([sqrt(j) for j in f])
saving = [s*i-c_r*sqrt(j)*sigma_sqrt_fi for i, j in zip(picks, f)]
print(saving)
print(sigma_sqrt_fi)
print(f)
