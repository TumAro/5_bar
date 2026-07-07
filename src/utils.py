from pathlib import Path
import tomllib

def load_config():
    cfg_path = Path(__file__).parent.parent / "config.toml"
    with open(cfg_path, "rb") as f:
        return tomllib.load(f)

def clamp(v): return max(-1.0, min(1.0, v))
