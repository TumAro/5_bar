from math import acos, atan2, sqrt, pi
from utils import clamp
import tomli

with open("../config.toml", "rb") as f:
    config = tomli.load(f)

l = config["links"]["PROXIMAL"]
r = config["links"]["DISTAL"]
b = config["links"]["BASE"]

def inverse(x: float, y: float):
    d_L = sqrt(x**2 + y**2)
    d_R = sqrt((b-x)**2 + y**2)

    a_L = acos((l**2 + d_L**2 - r**2)/ (2*l*d_L))
    a_L = clamp(a_L)
    b_L = atan2(y,x)

    a_R = acos((l**2 + d_R**2 - r**2)/ (2*l*d_R))
    a_R = clamp(a_R)
    b_R = atan2(y,(b-x))

    return a_L+b_L, pi-(a_R + b_R)
