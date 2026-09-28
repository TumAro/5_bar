import sys
from math import atan2, cos, sin
from pathlib import Path

import cv2

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_config

config = load_config()

L_ANCHOR_ID = 10
R_ANCHOR_ID = 11
L_CRANK_ID = 0
R_CRANK_ID = 1

THETA_OFFSET_L = config["vision"]["THETA_OFFSET_L"]
THETA_OFFSET_R = config["vision"]["THETA_OFFSET_R"]
CAM = config["vision"]["CAM"]

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
detector = cv2.aruco.ArucoDetector(aruco_dict, cv2.aruco.DetectorParameters())


def _markers(corners, ids):
    """id -> 4x2 corners, y flipped so angles run CCW like the kinematics."""
    if ids is None:
        return {}
    return {int(i): c[0] * [1, -1] for c, i in zip(corners, ids.flatten())}


def thetas_from_markers(m: dict):
    """marker corners -> (theta1, theta2), None per side if that marker's missing.

    Crank angle is the crank marker's own edge direction, so anchors only set the
    base direction and can sit anywhere fixed. Rotation survives parallax, positions don't.
    """
    if L_ANCHOR_ID not in m or R_ANCHOR_ID not in m:
        return None, None

    base = m[R_ANCHOR_ID].mean(axis=0) - m[L_ANCHOR_ID].mean(axis=0)
    rot = atan2(base[1], base[0])

    def angle(marker_id, offset):
        if marker_id not in m:
            return None
        edge = m[marker_id][1] - m[marker_id][0]  # top-left -> top-right
        a = atan2(edge[1], edge[0]) - rot + offset
        return atan2(sin(a), cos(a))

    return angle(L_CRANK_ID, THETA_OFFSET_L), angle(R_CRANK_ID, THETA_OFFSET_R)


def get_thetas(frame):
    corners, ids, _ = detector.detectMarkers(frame)
    theta1, theta2 = thetas_from_markers(_markers(corners, ids))
    return theta1, theta2, corners, ids


def main():
    cap = cv2.VideoCapture(CAM, cv2.CAP_V4L2)
    # OpenCV defaults to 640x480 (4:3, narrower view); ask for full 16:9 sensor width. MJPG needed for 1080p at 30 fps
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
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
