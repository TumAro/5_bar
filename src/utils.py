from pathlib import Path
from math import pi
import tomllib
import matplotlib.pyplot as plt
import mujoco

def load_config():
    cfg_path = Path(__file__).parent.parent / "config.toml"
    with open(cfg_path, "rb") as f:
        return tomllib.load(f)

def clamp(v): return max(-1.0, min(1.0, v))

def unwrap(angles):
    out = [angles[0]]
    for a in angles[1:]:
        diff = a - out[-1]
        if diff > pi:   a -= 2 * pi
        elif diff < -pi: a += 2 * pi
        out.append(a)
    return out

def plot(vals, title: str, xlabel: str, ylabel: str, marker="o"):
    plt.plot(vals, marker=marker)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()

def u2theta(u):
    return u[0] - pi/2, u[1] - pi/2

def theta2u(theta):
    return theta[0] + pi/2, theta[1] + pi/2

def read_state(model, data):
    jL = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "L_cranker_joint")
    jR = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_JOINT, "R_cranker_joint")
    return data.qpos[jL], data.qpos[jR]
