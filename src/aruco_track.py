import sys
from math import atan2
from pathlib import Path

import cv2
import numpy as np

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_config

config = load_config()
BASE_M = config["links"]["BASE"] / 1000

L_ANCHOR_ID = 10
R_ANCHOR_ID = 11
L_CRANK_ID = 0
R_CRANK_ID = 1

THETA_OFFSET_L = config["vision"]["THETA_OFFSET_L"]
THETA_OFFSET_R = config["vision"]["THETA_OFFSET_R"]

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())


def _centers(corners, ids):
    if ids is None:
        return {}
    return {int(i): np.array([c[0].mean(axis=0)[0], -c[0].mean(axis=0)[1]])
            for c, i in zip(corners, ids.flatten())}


def thetas_from_points(pts: dict):
    """pixel-center dict -> (theta1, theta2), None per side if that marker's missing."""
    if L_ANCHOR_ID not in pts or R_ANCHOR_ID not in pts:
        return None, None

    anchor_vec = pts[R_ANCHOR_ID] - pts[L_ANCHOR_ID]
    rot = atan2(anchor_vec[1], anchor_vec[0])

    theta1 = theta2 = None
    if L_CRANK_ID in pts:
        v = pts[L_CRANK_ID] - pts[L_ANCHOR_ID]
        theta1 = atan2(v[1], v[0]) - rot + THETA_OFFSET_L
    if R_CRANK_ID in pts:
        v = pts[R_CRANK_ID] - pts[R_ANCHOR_ID]
        theta2 = atan2(v[1], v[0]) - rot + THETA_OFFSET_R

    return theta1, theta2


def get_thetas(frame):
    corners, ids, _ = detector.detectMarkers(frame)
    pts = _centers(corners, ids)
    theta1, theta2 = thetas_from_points(pts)

    if L_ANCHOR_ID in pts and R_ANCHOR_ID in pts:
        px_base = np.linalg.norm(pts[R_ANCHOR_ID] - pts[L_ANCHOR_ID])
        if px_base < 1:
            print("warning: anchors basically coincident in frame, check marker placement")

    return theta1, theta2, corners, ids


def main():
    cap = cv2.VideoCapture(0)
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        theta1, theta2, corners, ids = get_thetas(frame)
        print(theta1, theta2)

        debug = frame.copy()
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(debug, corners, ids)
        cv2.imshow("aruco_track", debug)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
