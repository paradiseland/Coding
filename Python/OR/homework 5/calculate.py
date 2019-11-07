"""
prob:
max f(x1,x2) = -(x1-2)^2-x1-x2^2
begin at the point (2.5,1.5) 
"""
import sympy as sp

point = [2.5, 1.5]
x1, x2, t0 = sp.symbols("x1 x2 t0")
x = [x1, x2]
f_expr = -(x1-2)**2-x1-x2**2
f_gradient = [sp.diff(f_expr, x1), sp.diff(f_expr, x2)]
print("f_gradient:", f_gradient)
f_gradient_value = [f_gradient[i].subs(x[i], point[i]) for i in range(2)]
print('gradient:', f_gradient_value)
while f_gradient_value != [0, 0]:

    point = [(x[i]+f_gradient_value[i]*t0).subs([(x1, point[0]), (x2, point[1])])
             for i in range(2)]
    f_t0 = sp.expand(f_expr.subs([(x1, point[0]), (x2, point[1])]))
    t0_value = sp.solve(sp.diff(f_t0, t0), t0)
    points = [point[i].subs(t0, t0_value[0]) for i in range(2)]
    f_gradient_value = [f_gradient[i].subs(x[i], points[i]) for i in range(2)]
    print("point:", points)
    print("gradient:", f_gradient_value)

f_gradient: [-2*x1 + 3, -2*x2]
gradient: [-2.0, -3.0]
point: [1.5, 0]
gradient: [0, 0]
