from math import cos, sin, sqrt
from .utils import load_config

config = load_config()
l = config["links"]["PROXIMAL"]
r = config["links"]["DISTAL"]
b = config["links"]["BASE"]

def x_sol(y: float, th1: float, th2: float):
    num = b*b + 2*b*l*cos(th2) + 2*l*y*(sin(th1) - sin(th2))
    den = 2*b - 2*l*cos(th1) + 2*l*cos(th2)
    return num/den

def y_sol(th1: float, th2: float):
    A = 4*(b*b + 2*l*l*(1-cos(th1-th2)) +2*b*l*(cos(th2) - cos(th1)))
    B = 4*l*(-b*b +2*l*l*(cos(th1-th2)-1) +2*b*l*(cos(th1)-cos(th2)))*(sin(th1)+sin(th2))
    C = (b**4 - 4*b*b*r*r
         + 4*l**4*cos(th1)**4
         - 8*l**3*cos(th1)**3*(b + l*cos(th2))
         + 4*l*cos(th1)*(b + l*cos(th2))*(-b*b + l*l*(cos(2*th1)-1) + 2*r*r - 2*b*l*cos(th2))
         + 2*l*l*cos(th1)**2*(4*b*b + l*l*(1+cos(2*th2)) - 2*r*r + 8*b*l*cos(th2))
         + 4*b*b*l*l*sin(th1)**2
         + 4*l*l*cos(th2)**2*(b*b - r*r + l*l*sin(th1)**2)
         + 4*b*l*cos(th2)*(b*b - 2*r*r + 2*l*l*sin(th1)**2)
         + l**4*sin(2*th1)**2)

    discr = B*B-4*A*C
    if discr < 0: return (None, None)

    root1 = (-B+abs(sqrt(discr)))/(2*A)
    root2 = (-B-abs(sqrt(discr)))/(2*A)

    return (root1, root2)

def forward(th1: float, th2: float):
    y1, y2 = y_sol(th1, th2)
    x1, x2 = x_sol(y1, th1, th2), x_sol(y2, th1, th2)
    return ((x1,y1), (x2,y2))
