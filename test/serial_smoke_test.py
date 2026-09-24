import time

from src.serial_link import open_link, send_theta
from src.utils import u2theta
from test.circle import circle_trajectory

T = 8.0  # seconds for one full loop of the trajectory

if __name__ == "__main__":
    traj = circle_trajectory(N=800, timesteps=2)  # N pts, t*10 ms apart = servo frame rate
    dt = T / len(traj)

    ser = open_link()
    for theta1, theta2 in traj:
        send_theta(ser, *u2theta((theta1, theta2)))  # circle_trajectory is in u (servo) angles
        time.sleep(dt)
    ser.close()
