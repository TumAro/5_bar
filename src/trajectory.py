import numpy as np
from typing import Tuple, List

def s(t: float):
    return 10*t**3 - 15*t**4 + 6*t**5

def ds(t: float):
    return 30*t**2 - 60*t**3 + 30*t**4

def dds(t: float):
    return 60*t - 180*t**2 + 120*t**3

def trajectory(start: Tuple[float, float], end: Tuple[float, float], timesteps=100, derivatives=False):
    """
    Minimum jerk trajectory in joint space.

    Returns list of (θ1, θ2) or (θ1, θ2, dθ1, dθ2, ddθ1, ddθ2) tuples.
    Velocity/acceleration are per unit normalized time; divide by duration T for rad/s.
    """
    d1 = end[0] - start[0]
    d2 = end[1] - start[1]
    path = []
    for t in np.linspace(0, 1, timesteps):
        th1 = start[0] + d1 * s(t)
        th2 = start[1] + d2 * s(t)
        if derivatives:
            path.append((th1, th2, d1*ds(t), d2*ds(t), d1*dds(t), d2*dds(t)))
        else:
            path.append((th1, th2))
    return path


def waypoint2traj(waypoints: List[Tuple[float, float]], timesteps: int = 100) -> List[Tuple[float, float]]:
    """Chain joint-space waypoints into one trajectory. Junction points not duplicated."""
    path = []
    for i in range(len(waypoints) - 1):
        seg = trajectory(waypoints[i], waypoints[i + 1], timesteps)
        path.extend(seg if i == len(waypoints) - 2 else seg[:-1])
    return path
