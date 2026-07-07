import numpy as np
from src import inverse, waypoint2traj, unwrap

def circle_trajectory(center: tuple[float, float] = (75, 250), radius: float = 100, N = 16):

    angles = np.linspace(0, 2 * np.pi, N, endpoint=False)
    
    x = center[0] + radius * np.cos(angles)
    y = center[1] + radius * np.sin(angles)
    points = list(np.column_stack((x, y)))
    
    inverse_x, inverse_y = zip(*[inverse(*pt) for pt in points])
    unwrapped = list(zip(unwrap(inverse_x), unwrap(inverse_y)))
    unwrapped.append(unwrapped[0])
    
    return waypoint2traj(unwrapped, timesteps=4000)