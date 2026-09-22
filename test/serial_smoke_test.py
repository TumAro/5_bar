import time

from src.serial_link import open_link, send_theta
from test.circle import circle_trajectory

T = 8.0  # seconds for one full loop of the trajectory

if __name__ == "__main__":
    traj = circle_trajectory()
    dt = T / len(traj)

    ser = open_link()
    for theta1, theta2 in traj:
        send_theta(ser, theta1, theta2)
        time.sleep(dt)
    ser.close()
