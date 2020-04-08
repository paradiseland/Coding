"""
Construct the travel time model. 
Compute the travel time given each parameters. 
"""
import sympy 
import numpy as np
import pandas  as pd

# AS/RS design
# AS/RS L:30 H:6 n_x:60 n_y:20 num_containers:2400
# S/R 
# v_x:2 a_+:1 a_x-:1 v_y:1.5 a_y+:.75 a_y-:.75

# Compute the condition in 1990 paper.

def get_time(L, H, v_x, v_y, acc_x, acc_y):
    t_L = L/v_x + v_x/acc_x
    t_H = H/v_y + v_y/acc_y
    t_l = 2*v_x/acc_x
    t_h = 2*v_y/acc_y
    return t_L, t_H, t_l, t_h


def get_condition(t_L, t_H, t_l, t_h):

    """
    given v_x > v_y => t_h < t_l
    """
    if t_h <= t_l:
    # t_h <= t_l <= t_L => 3 conditions. 
        if t_l <= t_H and t_H <= t_L:
            condition = 0
        elif t_h <= t_H and t_H <= t_l:
            condition = 1
        elif t_L <= t_H:
            condition = 2
    else:
    # t_l <= t_h <= t_H. 3 conditions. 
        if t_L <= t_h:
            condition = 3
        elif t_h <= t_L and t_L <= t_H:
            condition = 4
        elif t_H <= t_L:
            condition = 5
    return condition

def get_interval(t_L, t_H, t_l, t_h):
    if t_h <= t_l:
        if t_l <= t_H and t_H <= t_L:
            interval = [(0, t_h), (t_h, t_l), (t_l, t_H), (t_H, t_L)]
        elif t_h <= t_H and t_H <= t_l:
            interval = [(0, t_h), (t_h, t_H), (t_H, t_l), (t_l, t_L)]
        elif t_L <= t_H:
            interval = [(0, t_h), (t_h, t_l), (t_l, t_L), (t_L, t_H)]
    else:
        if t_L <= t_h:
            interval = [(0, t_l), (t_l, t_L), (t_L, t_h), (t_h, t_H)]
        elif t_h <= t_L and t_L <= t_H:
            interval = [(0, t_l), (t_l, t_h), (t_h, t_L), (t_L, t_H)]
        elif t_H <= t_L:
            interval = [(0, t_l), (t_l, t_h), (t_h, t_H), (t_H, t_L)]
    return interval



# 0 <= z <= t_h G1(z) = a**2*z**4 /16/L/H
def t_x_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return acc_x*z**2/(4*L)

def t_x_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1/L*(v_x*z - v_x**2/acc_x)

def t_y_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return acc_y*z**2/(4*H)

def t_y_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1/H*(v_y*z - v_y**2/acc_y)



def G1_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return  t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G1_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return  t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G1_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G1_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)

'''condition2 : t_h <= t_H <= t_l <= t_L'''
def G2_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G2_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G2_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*1

def G2_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*1


def G3_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G3_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G3_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G3_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return 1*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)


def G4_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G4_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G4_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G4_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)


def G5_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G5_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G5_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G5_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)


def G6_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_1(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G6_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_1(z, L, H, v_x, v_y, acc_x, acc_y)

def G6_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*t_y_2(z, L, H, v_x, v_y, acc_x, acc_y)

def G6_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_x_2(z, L, H, v_x, v_y, acc_x, acc_y)*1



def t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y): 
    return acc_x*z**2/(2*L) - acc_x**2*z**4/(16*L**2)

def t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y): 
    return -v_x**2/(L**2)*z**2+ (2*v_x/L+2*v_x**3/(acc_x*L**2))*z - 2*v_x**2/(acc_x*L) - v_x**4/(acc_x**2*L**2)

def t_by_th(z, L, H, v_x, v_y, acc_x, acc_y): 
    return acc_y*z**2/(2*H) - acc_y**2*z**4/(16*H**2)

def t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y): 
    return -v_y**2/(H**2)*z**2+ (2*v_y/H+2*v_y**3       /(acc_y*H**2))*z - 2*v_y**2/(acc_y*H) - v_y**4/(acc_y**2*H**2)  


def B1_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return  t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B1_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return  t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B1_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B1_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)


def B2_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B2_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B2_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*1

def B2_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*1


def B3_1(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B3_2(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B3_3(z, L, H, v_x, v_y, acc_x, acc_y): 
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B3_4(z, L, H, v_x, v_y, acc_x, acc_y): 
    return 1*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B4_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B4_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B4_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B4_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)


def B5_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B5_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B5_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B5_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return 1*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)


def B6_1(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tl(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B6_2(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_th(z, L, H, v_x, v_y, acc_x, acc_y)

def B6_3(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*t_by_tH(z, L, H, v_x, v_y, acc_x, acc_y)

def B6_4(z, L, H, v_x, v_y, acc_x, acc_y):
    return t_bx_tL(z, L, H, v_x, v_y, acc_x, acc_y)*1


# P_Ta, P_Tv, P_B, t_acc, t_con, t_dec.

def get_P(m, k_r, g, acc_x, k_ir, v_x, v_y, eta):
    """
    give operation parameters, get the power.
    """
    # 1 N*m/s = 1 KW
    M = m + SR
    P_Ta = (M*g*k_r + M*acc_x*k_ir)*v_x/(1000*eta)
    P_Tv = M*g*k_r*v_x/(1000*eta)
    P_B = (M*acc_x*k_ir - M*g*k_r)*v_x/(1000*eta)
    
    t_acc = v_x/acc_x
    t_dec = v_x/acc_x
    t_con = (2/3*L - v_x**2/(2*acc_x) - v_x**2/(2*acc_x)) / v_x
    P_x = ((P_Ta**2*t_acc+P_Tv**2*t_con+P_B**2*t_dec)/(t_acc+t_con+t_dec))**.5
    P_y =  m*g*v_y/(1000*eta)
    P = P_x + P_y
    
    return P_x, P_y, P

def get_EnergyConsumption(P, T_shift, n_wd, n_weeks, epsilon, rho):
    """
    give the power in horizontal and vertical direction, get the energy consumption.
    """
    W = P * T_shift * n_wd * n_weeks * epsilon
    E_co2 = W * rho
    S_forest = E_co2 /10
    S_forest_ha = E_co2 /10 /10000
    S_football = S_forest/7140
    return W, E_co2, S_forest, S_forest_ha, S_football


# P_y = G*r/r*v_y/1000/eta2

if __name__ == "__main__":
    eta_warehouse = .95
    T_handling = 10.62

    T_shift = 16
    n_wd = 5
    n_weeks = 50
    epsilon = .8
    rho = .59
    gravity = 10 
    k_r = 10.5 / 1000
    k_ir = 1.15
    eta = .9
    mass = 300
    # generate different designs of warehouse configuration and operation.
    L_H = [(30, 6, 450), (45, 10.2, 750), (60, 13.2, 975)]
    v_xy = [(2, 1.5)]*4 + [(4, 1.5)]*6 + [(4, 3)]*6 + [(6, 3), (6.5, 3.5)]
    a_xy = [(1, .75), (1, 1.5), (2, .75), (2, 1.5)]*2 + [(3, .75), (3, 1.5), (1, 1.5), (1, 2.25), (2, 1.5), (2, 2.25), (3, 1.5), (3, 2.25), (3, 3), (6.5, 3.5)]
    v_a = [v+a for v,a in zip(v_xy, a_xy)]
    design = [[] for i in range(len(L_H)*len(v_a))]

    for ind, k in enumerate(L_H):
        for ind1, i in enumerate(v_a):
            design[len(v_a)*ind+ind1].append(k)
            design[len(v_a)*ind+ind1].append(i)
            design[len(v_a)*ind+ind1] = [m for n in design[len(v_a)*ind+ind1] for m in n]
    z = sympy.symbols('z')
    f = open('EnergyConsumption.txt', 'w')
    DC = []
    throughput = []
    Watt = []
    co2_emission = []
    for index, des in enumerate(design):
        L, H, SR, v_x, v_y, acc_x, acc_y = des
        t_L, t_H, t_l, t_h = get_time(L, H, v_x, v_y, acc_x, acc_y)  
        # print("L={}, H={}, v_x={}, v_y={}, acc={}".format(L, H, v_x, v_y, acc))
        warehouse_design = "{}----------------------------------------------------\nL={}, H={}, m={}, v_x={}, v_y={}, acc_x={}, acc_y={}".format(index+1, L, H, mass, v_x, v_y, acc_x, acc_y)
        # print("t_L={}, t_H={}, t_l={}, t_h={}".format(t_L, t_H, t_l, t_h))
        time = "\nt_L={:.3f}, t_H={:.3f}, t_l={:.3f}, t_h={:.3f}".format(t_L, t_H, t_l, t_h)
        # set(condition) = {0, 1, 5}
        condition = get_condition(t_L, t_H, t_l, t_h)

        cond = '\ncondition:{}\n'.format(condition)
        interval = get_interval(t_L, t_H, t_l, t_h)
        inte = 'interval: '
        for t in interval:
            inte += '[{:.3f}, {:.3f}], '.format(t[0], t[1]) 

        G1 = [G1_1, G1_2, G1_3, G1_4]
        G2 = [G2_1, G2_2, G2_3, G2_4]
        G3 = [G3_1, G3_2, G3_3, G3_4]
        G4 = [G4_1, G4_2, G4_3, G4_4]
        G5 = [G6_1, G6_2, G6_3, G5_4]
        G6 = [G6_1, G6_2, G6_3, G6_4]
        G = [G1, G2, G3, G4, G5, G6]

        g1 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G1]
        g2 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G2]
        g3 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G3]
        g4 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G4]
        g5 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G5]
        g6 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in G6]

        g = [g1, g2, g3, g4, g5, g6]

        g_select = g[condition]

        integrate = [sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(g_select)]

        expection_OT = sum([sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(g_select)])

        B1 = [B1_1, B1_2, B1_3, B1_4]
        B2 = [B2_1, B2_2, B2_3, B2_4]
        B3 = [B3_1, B3_2, B3_3, B3_4]
        B4 = [B4_1, B4_2, B4_3, B4_4]
        B5 = [B5_1, B5_2, B5_3, B5_4]
        B6 = [B6_1, B6_2, B6_3, B6_4]
        B = [B1, B2, B3, B4, B5, B6]

        b1 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B1]
        b2 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B2]
        b3 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B3]
        b4 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B4]
        b5 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B5]
        b6 = [sympy.diff(i(z, L, H, v_x, v_y, acc_x, acc_y), z) for i in B6]
        b = [b1, b2, b3, b4, b5, b6]

        b_select = b[condition]

        expection_TB = sum([sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(b_select)])
        expection_DC = 2*expection_OT + expection_TB + T_handling
        # print("E(OT)={}".format(expection_OT))
        EDC = "\nE(DC)={:.3f}".format(expection_DC)
        Throughput = "\nThroughput = {}".format(round(3600/expection_DC*2*eta_warehouse))
        P_x, P_y, P = get_P(mass, k_r, gravity, acc_x, k_ir, v_x, v_y, eta)
        power = '\nP_x={:.2f} kW, P_y={:.2f} kW, P={:.2f} kW'.format(P_x, P_y, P)
        W, E_co2, S_forest, S_forest_ha, S_football = get_EnergyConsumption(P, T_shift, n_wd, n_weeks, epsilon, rho)
        Consumption = '\nW={:.0f} kW, E_CO2={:.0f} kgCo2/year, S_forest = {:.0f} m^2/10years = {:.2f} ha/10years, S_football ={:.2f} \n\n'.format(W, E_co2, S_forest, S_forest_ha, S_football)
        throughput.append(round(3600/expection_DC*2*eta_warehouse))
        DC.append(expection_DC)
        Watt.append(W)
        co2_emission.append(E_co2)
        f.write(warehouse_design)
        f.write(time)
        f.write(cond)
        f.write(inte)
        f.write(EDC)
        f.write(Throughput)
        f.write(power)
        f.write(Consumption)
    f.close()
    para = [throughput, DC, Watt, co2_emission]

    plot = open('plot_paras.txt', 'w')
    for i in para:
        for j in i:
            plot.write(str(j)+' ')
        plot.write('\n')
    plot.close()
