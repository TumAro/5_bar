from math import acos, atan2, sqrt, pi
from .utils import load_config

config = load_config()
l = config["links"]["PROXIMAL"]
r = config["links"]["DISTAL"]
b = config["links"]["BASE"]

def inverse(x: float, y: float):
    d_L = sqrt(x**2 + y**2)
    d_R = sqrt((b-x)**2 + y**2)

    if d_L < 1e-9 or d_R < 1e-9:
        raise ValueError(f"EE at motor origin: ({x}, {y})")

    cos_L = (l**2 + d_L**2 - r**2) / (2*l*d_L)
    cos_R = (l**2 + d_R**2 - r**2) / (2*l*d_R)

    if abs(cos_L) > 1.0 or abs(cos_R) > 1.0:
        raise ValueError(f"Point ({x}, {y}) outside workspace")

    a_L = acos(cos_L)
    b_L = atan2(y, x)

    a_R = acos(cos_R)
    b_R = atan2(y, (b-x))

    return a_L + b_L, pi - (a_R + b_R)
