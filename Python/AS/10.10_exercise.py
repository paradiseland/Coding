import numpy as np
from scipy.integrate import tplquad,dblquad,quad

Ex = dblquad(lambda y, x: x * 0.5*(1/np.pi) *
                                 np.exp(-0.5*(2*pow(x, 2)+pow(y, 2)+2*x*y-22*x-14*y+65)),
                    float('-inf'),
                    float('inf'),
                    float('-inf'),
                    float('inf'))
Ey = dblquad(lambda y, x:  y * 0.5*(1/np.pi) *
                                 np.exp(-0.5*(2*pow(x, 2)+pow(y, 2)+2*x*y-22*x-14*y+65)),
                    float('-inf'),
                    float('inf'),
                    float('-inf'),
                    float('inf'))
Ex2 = dblquad(lambda y, x: pow(x, 2) * 0.5*(1/np.pi) *
                                 np.exp(-0.5*(2*pow(x, 2)+pow(y, 2)+2*x*y-22*x-14*y+65)),
                    float('-inf'),
                    float('inf'),
                    float('-inf'),
                    float('inf'))
sigma_x = Ex2[0]-pow(Ex[0],2)
Ey2 = dblquad(lambda y, x: pow(y, 2) * 0.5*(1/np.pi) *
                                 np.exp(-0.5*(2*pow(x, 2)+pow(y, 2)+2*x*y-22*x-14*y+65)),
                    float('-inf'),
                    float('inf'),
                    float('-inf'),
                    float('inf'))
sigma_y = Ey2[0]-pow(Ey[0],2)
Exy = dblquad(lambda y, x: x * y * 0.5*(1/np.pi) *
                                 np.exp(-0.5*(2*pow(x, 2)+pow(y, 2)+2*x*y-22*x-14*y+65)),
                    float('-inf'),
                    float('inf'),
                    float('-inf'),
                    float('inf'))
sigma_xy = Exy[0]-Ex[0]*Ey[0]
rho_xy = sigma_xy/(np.sqrt(sigma_x)*np.sqrt(sigma_y))

print('Ex:{}\nEy:{}\nEx2:{}\nEy2:{}\nExy:{}\nsigma_x:{}\nsigma_y:{}\nsigma_xy:{}\nrhoxy:{}'.format(
    Ex[0], Ey[0], Ex2[0], Ey2[0], Exy[0], sigma_x,sigma_y, sigma_xy, rho_xy))

a = np.matrix([1],[])
"""
Ex:3.999999999728539
Ey:3.000000000014267
Ex2:17.000000000071108
Ey2:10.99999999957127
Exy:11.000000000132411
sigma_x:1.0000000022427962
sigma_y:1.9999999994856683
sigma_xy:-0.9999999991102726
rhoxy:-0.707106779855389  -> -sqrt(2)/2
SIGMA = [[1,-1],[-1,2]]
SIGMA^-1 = [[2,1],[1,1]]
|SIGMA| = 1
"""



