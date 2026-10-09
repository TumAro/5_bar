
import time, csv
from math import degrees

from src.serial_link import open_link, send_theta
from src.utils import u2theta
from test.circle import circle_trajectory

from src import aruco_track as at

LOOPS = 3  # number of loop
T = 8 # total second of each loop

if __name__ == "__main__":
    rows = []
    traj = circle_trajectory(N=800, timesteps=2)

    ser = open_link()
    cap = at.open_camera()

    t0 = time.time()
    while True:
        t = time.time() - t0            
        u = traj[int(t / T * len(traj)) % len(traj)]
        if t >= LOOPS * T: break
        
        send_theta(ser, *u2theta(u))       
                   
        ok, frame = cap.read()
        if not ok:
            break
        cam1, cam2, corners, ids = at.get_thetas(frame)
        if cam1 is not None and cam2 is not None:
            print(f"theta1 : {cam1:.2f} | theta2: {cam2:.2f} \ncmd1 : {u[0]:.2f} | cmd2 : {u[1]:.2f}")

        rows.append((t,u[0],u[1],cam1,cam2))

    cap.release()
    send_theta(ser, 0,0)
    ser.close()

    with open("notebooks/sim2real_log.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["t", "cmd1", "cmd2", "cam1", "cam2"])
        w.writerows(rows)
        print("LOG saved to report/sim2real_log.csv")
