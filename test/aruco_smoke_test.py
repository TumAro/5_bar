import time
from math import degrees

import cv2

from src import aruco_track as at
from src.serial_link import open_link, send_theta
from src.utils import u2theta
from test.circle import circle_trajectory

T = 8.0    # seconds per circle loop

if __name__ == "__main__":
    loop = circle_trajectory(N=400, timesteps=2)
    traj = loop + loop[::-1]  # one loop forward, one back
    ser = open_link()
    cap = cv2.VideoCapture(at.CAM, cv2.CAP_V4L2)
    # OpenCV defaults to 640x480 (4:3, narrower view); ask for full 16:9 sensor width. MJPG needed for 1080p at 30 fps
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
    win = "aruco_smoke_test (q to quit)"
    cv2.namedWindow(win, cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.setWindowProperty(win, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    t0 = time.time()
    while True:
        # pick the point for the current time, so slow camera frames skip points instead of slowing the arm
        u = traj[int((time.time() - t0) / (2 * T) * len(traj)) % len(traj)]
        send_theta(ser, *u2theta(u))
        ser.reset_input_buffer()  # pot replies aren't used here

        ok, frame = cap.read()
        if not ok:
            break
        theta1, theta2, corners, ids = at.get_thetas(frame)
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(frame, corners, ids)
        fmt = lambda a: "--" if a is None else f"{degrees(a):6.1f}"
        for row, text in enumerate([f"cmd  L {degrees(u[0]):6.1f}  R {degrees(u[1]):6.1f}",
                                    f"cam  L {fmt(theta1)}  R {fmt(theta2)}"]):
            cv2.putText(frame, text, (10, 30 + 30 * row), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.imshow(win, frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    send_theta(ser, 0, 0)  # home: both cranks forward
    ser.close()
    cap.release()
    cv2.destroyAllWindows()
