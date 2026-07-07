from pathlib import Path
from math import pi
import tomllib

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
