import time, csv
from math import degrees

from src.serial_link import open_link, send_theta
from src.utils import u2theta
from test.circle import circle_trajectory

from src import aruco_track as at
from src.serial_link import OFFSET_L, OFFSET_R


LOOPS = 10
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

    out = time.strftime(f"notebooks/data/sim2real_{LOOPS}_%Y%m%d_%H%M%S.csv")
    with open(out, "w", newline="") as f:
        # calibration used for this run; read the CSV with pd.read_csv(out, comment="#")
        f.write(f"# THETA_OFFSET_L={at.THETA_OFFSET_L} THETA_OFFSET_R={at.THETA_OFFSET_R} "
                f"OFFSET_L={OFFSET_L} OFFSET_R={OFFSET_R} T={T} LOOPS={LOOPS}\n")
        w = csv.writer(f)
        w.writerow(["t", "cmd1", "cmd2", "cam1", "cam2"])
        w.writerows(rows)
        print(f"LOG saved to {out}")
