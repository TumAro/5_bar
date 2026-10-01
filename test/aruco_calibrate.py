import re
import time
from math import degrees, pi
from pathlib import Path

from src import aruco_track as at
from src.serial_link import open_link, send_theta

FRAMES = 30  # averaged at home pose

if __name__ == "__main__":
    ser = open_link()
    send_theta(ser, 0, 0)  # home: both cranks forward (servo offsets already applied)
    time.sleep(2)
    cap = at.open_camera()
    raw_l, raw_r = [], []
    while len(raw_l) < FRAMES:
        ok, frame = cap.read()
        if not ok:
            raise RuntimeError("no camera frames (camera busy?)")
        t1, t2, _, _ = at.get_thetas(frame)
        if t1 is not None and t2 is not None:
            raw_l.append(t1 - at.THETA_OFFSET_L)
            raw_r.append(t2 - at.THETA_OFFSET_R)
    cap.release()
    ser.close()

    # home pose is pi/2 (crank pointing forward) in the kinematics
    off_l = pi / 2 - sum(raw_l) / FRAMES
    off_r = pi / 2 - sum(raw_r) / FRAMES
    spread = degrees(max(max(raw_l) - min(raw_l), max(raw_r) - min(raw_r)))
    cfg = Path(__file__).parent.parent / "config.toml"
    text = re.sub(r"^THETA_OFFSET_L = .*$", f"THETA_OFFSET_L = {off_l:.4f}", cfg.read_text(), flags=re.M)
    text = re.sub(r"^THETA_OFFSET_R = .*$", f"THETA_OFFSET_R = {off_r:.4f}", text, flags=re.M)
    cfg.write_text(text)
    print(f"THETA_OFFSET_L = {off_l:.4f} ({degrees(off_l):.1f} deg)")
    print(f"THETA_OFFSET_R = {off_r:.4f} ({degrees(off_r):.1f} deg)")
    print(f"frame-to-frame spread {spread:.2f} deg, written to config.toml")
