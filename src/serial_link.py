import sys
import time
from math import pi
from pathlib import Path

import serial

sys.path.insert(0, str(Path(__file__).parent.parent))
from src.utils import load_config, theta2u

config = load_config()
JOINT_SOFT = config["limits"]["JOINT_SOFT"]
OFFSET_L = config["servo"]["OFFSET_L"]
OFFSET_R = config["servo"]["OFFSET_R"]


def open_link():
    cfg = config["serial"]
    ser = serial.Serial(cfg["PORT"], cfg["BAUD"], timeout=1)
    time.sleep(2)  # let the Arduino reset after the port opens
    return ser


def send_theta(ser, theta1: float, theta2: float):
    theta1 = max(-JOINT_SOFT, min(JOINT_SOFT, theta1))
    theta2 = max(-JOINT_SOFT, min(JOINT_SOFT, theta2))
    u1, u2 = theta2u((theta1, theta2))
    deg1 = u1 * 180 / pi + OFFSET_L
    deg2 = u2 * 180 / pi + OFFSET_R
    ser.write(f"{deg1:.2f},{deg2:.2f}\n".encode())
