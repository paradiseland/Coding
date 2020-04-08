"""
Construct the travel time model. 
Compute the travel time given each parameters. 
"""
import sympy
import numpy as np
import pandas  as pd

# AS/RS design


def get_time(L, H, v_x, v_y, acc):
    t_L = L/v_x + v_x/acc
    t_H = H/v_y + v_y/acc
    t_l = 2*v_x/acc
    t_h = 2*v_y/acc
    return t_L, t_H, t_l, t_h


def get_condition(t_L, t_H, t_l, t_h):
    """
    Compute the condition in 1990 paper.
    """

    if t_l <= t_H and t_H <= t_L:
        condition = 0
    elif t_h <= t_H and t_H <= t_l:
        condition = 1
    elif t_L <= t_H:
        condition = 2
    else: 
        pass
    return condition

def get_interval(t_L, t_H, t_l, t_h):
    """
    Get the integrate interval.                     
    """
    if t_l <= t_H and t_H <= t_L:
        interval = [(0, t_h), (t_h, t_l), (t_l, t_H), (t_H, t_L)]
    elif t_h <= t_H and t_H <= t_l:
        interval = [(0, t_h), (t_h, t_H), (t_H, t_l), (t_l, t_L)]
    elif t_L <= t_H:
        interval = [(0, t_h), (t_h, t_l), (t_l, t_L), (t_L, t_H)]
    else: 
        pass
    return interval



# 0 <= z <= t_h G1(z) = a**2*z**4 /16/L/H

def t_x_1(z, L, H, v_x, v_y, acc): 
    return acc*z**2/(4*L)

def t_x_2(z, L, H, v_x, v_y, acc):
    return 1/L*(v_x*z - v_x**2/acc)

def t_y_1(z, L, H, v_x, v_y, acc):
    return acc*z**2/(4*H)

def t_y_2(z, L, H, v_x, v_y, acc):
    return 1/H*(v_y*z - v_y**2/acc)


def G1_1(z, L, H, v_x, v_y, acc): 
    return  t_x_1(z, L, H, v_x, v_y, acc)*t_y_1(z, L, H, v_x, v_y, acc)

def G1_2(z, L, H, v_x, v_y, acc): 
    return  t_x_1(z, L, H, v_x, v_y, acc)*t_y_2(z, L, H, v_x, v_y, acc)

def G1_3(z, L, H, v_x, v_y, acc): 
    return  t_x_2(z, L, H, v_x, v_y, acc)*t_y_2(z, L, H, v_x, v_y, acc)

def G1_4(z, L, H, v_x, v_y, acc): 
    return  t_x_2(z, L, H, v_x, v_y, acc)

def G2_1(z, L, H, v_x, v_y, acc): 
    return t_x_1(z, L, H, v_x, v_y, acc)*t_y_1(z, L, H, v_x, v_y, acc)

def G2_2(z, L, H, v_x, v_y, acc): 
    return t_x_1(z, L, H, v_x, v_y, acc)*t_y_2(z, L, H, v_x, v_y, acc)

def G2_3(z, L, H, v_x, v_y, acc): 
    return t_x_1(z, L, H, v_x, v_y, acc)*1

def G2_4(z, L, H, v_x, v_y, acc): 
    return t_x_2(z, L, H, v_x, v_y, acc)*1

def G3_1(z, L, H, v_x, v_y, acc): 
    return t_x_1(z, L, H, v_x, v_y, acc)*t_y_1(z, L, H, v_x, v_y, acc)

def G3_2(z, L, H, v_x, v_y, acc): 
    return t_x_1(z, L, H, v_x, v_y, acc)*t_y_2(z, L, H, v_x, v_y, acc)

def G3_3(z, L, H, v_x, v_y, acc): 
    return t_x_2(z, L, H, v_x, v_y, acc)*t_y_2(z, L, H, v_x, v_y, acc)

def G3_4(z, L, H, v_x, v_y, acc): 
    return 1*t_y_2(z, L, H, v_x, v_y, acc)



def t_bx_tl(z, L, H, v_x, v_y, acc): 
    return acc*z**2/(2*L) - acc**2*z**4/(16*L**2)

def t_bx_tL(z, L, H, v_x, v_y, acc): 
    return -v_x**2/(L**2)*z**2+ (2*v_x/L+2*v_x**3/(acc*L**2))*z - 2*v_x**2/(acc*L) - v_x**4/(acc**2*L**2)

def t_by_th(z, L, H, v_x, v_y, acc): 
    return acc*z**2/(2*H) - acc**2*z**4/(16*H**2)

def t_by_tH(z, L, H, v_x, v_y, acc): 
    return -v_y**2/(H**2)*z**2+ (2*v_y/H+2*v_y**3/(acc*H**2))*z - 2*v_y**2/(acc*H) - v_y**4/(acc**2*H**2)  


def B1_1(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_th(z, L, H, v_x, v_y, acc)

def B1_2(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_tH(z, L, H, v_x, v_y, acc)

def B1_3(z, L, H, v_x, v_y, acc): 
    return t_bx_tL(z, L, H, v_x, v_y, acc) * t_by_tH(z, L, H, v_x, v_y, acc)

def B1_4(z, L, H, v_x, v_y, acc): 
    return t_bx_tL(z, L, H, v_x, v_y, acc)


def B2_1(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_th(z, L, H, v_x, v_y, acc)

def B2_2(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_tH(z, L, H, v_x, v_y, acc)

def B2_3(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * 1

def B2_4(z, L, H, v_x, v_y, acc): 
    return t_bx_tL(z, L, H, v_x, v_y, acc) * 1



def B3_1(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_th(z, L, H, v_x, v_y, acc)

def B3_2(z, L, H, v_x, v_y, acc): 
    return t_bx_tl(z, L, H, v_x, v_y, acc) * t_by_tH(z, L, H, v_x, v_y, acc)

def B3_3(z, L, H, v_x, v_y, acc): 
    return t_bx_tL(z, L, H, v_x, v_y, acc) * t_by_tH(z, L, H, v_x, v_y, acc)

def B3_4(z, L, H, v_x, v_y, acc): 
    return t_by_tH(z, L, H, v_x, v_y, acc)



if __name__ == "__main__":
    a = [.5, .6, .7, .8, .9]
    L, H, v_x, v_y = 60, 20, 5, 2
    z = sympy.symbols('z')
    f = open('TravelTimeModel.txt', 'w')
    for acceleration in a:
        acc = acceleration
        t_L, t_H, t_l, t_h = get_time(L, H, v_x, v_y, acc)  
        # print("L={}, H={}, v_x={}, v_y={}, acc={}".format(L, H, v_x, v_y, acc))
        warehouse_design = "L={}, H={}, v_x={}, v_y={}, acc={}".format(L, H, v_x, v_y, acc)
        # print("t_L={}, t_H={}, t_l={}, t_h={}".format(t_L, t_H, t_l, t_h))
        time = "\nt_L={:.3f}, t_H={:.3f}, t_l={:.3f}, t_h={:.3f}".format(t_L, t_H, t_l, t_h)
        condition = get_condition(t_L, t_H, t_l, t_h)
        cond = '\ncondition:{}\n'.format(condition)
        interval = get_interval(t_L, t_H, t_l, t_h)
        inte = 'interval: '
        for t in interval:
            inte += '[{:.3f}, {:.3f}], '.format(t[0], t[1]) 

        G1 = [G1_1, G1_2, G1_3, G1_4]
        G2 = [G2_1, G2_2, G2_3, G2_4]
        G3 = [G3_1, G3_2, G3_3, G3_4]
        G = [G1, G2, G3]

        g1 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in G1]
        g2 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in G2]
        g3 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in G3]
        g = [g1, g2, g3]

        g_select = g[condition]

        integrate = [sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(g_select)]

        expection_OT = sum([sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(g_select)])

        B1 = [B1_1, B1_2, B1_3, B1_4]
        B2 = [B2_1, B2_2, B2_3, B2_4]
        B3 = [B3_1, B3_2, B3_3, B3_4]
        B = [B1, B2, B3]

        b1 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in B1]
        b2 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in B2]
        b3 = [sympy.diff(i(z, L, H, v_x, v_y, acc), z) for i in B3]
        b = [b1, b2, b3]

        b_select = b[condition]

        TB_integrate = [sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(b_select)]

        expection_TB = sum([sympy.integrate(z*f, (z, interval[ind]))  for ind, f in enumerate(b_select)])
        expection_DC = 2*expection_OT + expection_TB 
        # print("E(OT)={}".format(expection_OT))
        EOT = "\nE(OT)={:.3f}".format(expection_OT)
        ETB = '\nE(TB)={:.3f}\n\n'.format(expection_TB)
        f.write(warehouse_design)
        f.write(time)
        f.write(cond)
        f.write(inte)
        f.write(EOT)
        f.write(ETB)

    f.close()
