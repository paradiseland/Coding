from sympy import *
import math
import numpy as np
from sympy.abc import x, y

def obj1(x, y):
    z = -2 * x ** 2 - y ** 2 + x * y + 5
    return z

def constrain(x, y):
    first_constrain = x + y
    second_constrain = y
    return first_constrain, second_constrain

def diff1(z,k):
    dk = diff(z, k)
    return dk

def newobj1(obj1, first_constrain, second_constrain, m1, m2):
    newobj = obj1 - m1 * first_constrain - m2 * second_constrain
    return newobj

def Hessonandgrad():
    obj = obj1(x, y)
    first_constrain, second_constrain = constrain(x, y)
    newobj = newobj1(obj, first_constrain, second_constrain, m1, m2)
    dx = diff1(newobj, x)
    dy = diff1(newobj, y)
    dxdx = diff1(dx, x)
    dxdy = diff1(dx, y)
    dydx = diff1(dy, x)
    dydy = diff1(dy, y)
    dxdm1 = diff1(dx, m1)
    dxdm2 = diff1(dx, m2)
    dydm1 = diff1(dy, m1)
    dydm2 = diff1(dy, m2)
    constrain1 = -m1 * first_constrain
    constrain2 = -m2 * second_constrain
    dcon1dx = diff1(constrain1, x)
    dcon1dy = diff1(constrain1, y)
    dcon2dx = diff1(constrain2, x)
    dcon2dy = diff1(constrain2, y)
    dcon1dm1 = diff1(constrain1, m1)
    dcon1dm2 = diff1(constrain1, m2)
    dcon2dm1 = diff1(constrain2, m1)
    dcon2dm2 = diff1(constrain2, m2)
    Hesson = [[dxdx, dxdy, dxdm1, dxdm2], 
              [dydx, dydy, dydm1, dydm2], 
              [dcon1dx, dcon1dy, dcon1dm1, dcon1dm2],
              [dcon2dx, dcon2dy, dcon2dm1, dcon2dm2]]
    grad1 = -dx
    grad2 = -dy
    grad3 = u - constrain1
    grad4 = u - constrain2
    grad = np.array([[grad1],[grad2],[grad3],[grad4]])
    return Hesson,grad

def valuegrad(a,b,c,d,e,grad):
    gradarr = []
    for i in range(len(grad)):
        gradarr.append(float(grad[i][0].subs({x: a, y: b, m1: c, m2: d, u: e})))
    return gradarr

def valueHesson(a,b,c,d,Hesson):
    valHesson = [[0]*len(grad) for _ in range(len(grad))]
    for i in range(len(grad)):
        for j in range(len(grad)):
            valHesson[i][j] = float(Hesson[i][j].subs({x: a, y: b, m1: c, m2: d}))
    return valHesson

def valuedelta(a, b, c, d, e, grad, Hesson):
    gradnew = valuegrad(a,b,c,d,e,grad)
    Hessonnew = valueHesson(a,b,c,d,Hesson)
    invHesson = np.linalg.inv(Hessonnew)
    delta = np.dot(invHesson, gradnew)
    return delta

def deltanew1(a,b,c,d,delta):
    deltanew = []
    deltanew.append(a + delta[0] * t)
    deltanew.append(b + delta[1] * t)
    deltanew.append(c + delta[2] * t)
    deltanew.append(d + delta[3] * t)
    return deltanew

def newton(a, b, c, d, e, deltatemp, delta, t):
    obj = obj1(deltatemp[0],deltatemp[1])
    first_constrain, second_constrain = constrain(deltatemp[0], deltatemp[1])
    newobj = newobj1(obj, first_constrain, second_constrain, deltatemp[2], deltatemp[3])
    diffnewobj = diff1(newobj, t)
    result_t = solve(diffnewobj, t)[0]
    print("迭代步长为：")
    print(result_t)
    a = a + delta[0] * result_t
    b = b + delta[1] * result_t
    c = c + delta[2] * result_t
    d = d + delta[3] * result_t
    print("迭代后的值：")
    print(obj.subs({t: result_t}))
    e = e * 0.1
    delta = valuedelta(a, b, c, d, e, grad, Hesson)
    deltatemp = deltanew1(a,b,c,d,delta)

    print("迭代方向为：")
    print(delta)
    flag1 = delta[0]
    flag2 = delta[1]
    flag3 = delta[2]
    flag4 = delta[3]
    print("lambda",deltatemp[2],deltatemp[3])
    print("判断条件：")
    print(flag1, flag2, flag3, flag4)
    if abs(flag1) > alpha or abs(flag2) > alpha:
        newton(a, b, c, d, e, deltatemp, delta, t)
    print(a,b,c,d)


if __name__ == "__main__":
    alpha = 10e-5
    x, y = symbols('x, y')
    m1, m2 = symbols('m1, m2')
    u = symbols('u')
    t = symbols("t")
    Hesson, grad = Hessonandgrad()
    # 输入初始点
    a = -1
    b = -1
    c = -1
    d = -1
    e = 1
    # newton method get the delta /step
    delta = valuedelta(a, b, c, d, e, grad, Hesson)
    # get the new variable such as x,y,m1,m2
    deltatemp = deltanew1(a, b, c, d, delta)

    newton(a, b, c, d, e, deltatemp, delta, t)
    
