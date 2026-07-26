import cv2
import numpy as np

aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)

# name, id, print size (mm) -- pixel count is arbitrary, print dialog sets the real size
markers = [
    ("anchor_left_30mm", 10, 30),
    ("anchor_right_30mm", 11, 30),
    ("crank_left_15mm", 0, 15),
    ("crank_right_15mm", 1, 15),
    ("end_effector_spare_15mm", 2, 15),
]

for name, marker_id, _size_mm in markers:
    marker = cv2.aruco.generateImageMarker(aruco_dict, marker_id, 200)
    pad = 40
    canvas = np.full((200 + 2 * pad, 200 + 2 * pad), 255, dtype=np.uint8)
    canvas[pad:pad + 200, pad:pad + 200] = marker
    cv2.imwrite(f"markers/{name}.png", canvas)
