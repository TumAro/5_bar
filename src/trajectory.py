import numpy as np
from typing import Tuple, List

def s(t: float):
    return 10*t**3 -15*t**4 +6*t**5

# The trajectory is calculated in jointspace
def trajectory(start: Tuple[float, float], end: Tuple[float, float], timesteps=100, derivatives=False):
    """
    Compute minimum jerk trajectory in joint space.

    Args:
        start: (θ1, θ2) at t=0
        end:   (θ1, θ2) at t=1
        timesteps: number of points along path
        derivatives: if True -> returns  vel + acc

    Returns:
        list of (θ1, θ2) or (θ1, θ2, ds, dds) tuples
    """
    
    path = []
    for t in np.linspace(0,1,timesteps):
        th1 = start[0] + (end[0] - start[0])*s(t)
        th2 = start[1] + (end[1] - start[1])*s(t)
        if derivatives:
            path.append((th1, th2, ds(t), dds(t)))
        else:
            path.append((th1, th2))
    return path
        