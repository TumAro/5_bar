import mujoco
import mujoco.viewer
import numpy as np
from test import circle_trajectory

model = mujoco.MjModel.from_xml_path("five_bar.xml")
data = mujoco.MjData(model)

servo_L = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_L")
servo_R = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_R")

def main(n):
    trajectory = circle_trajectory()
    n = len(trajectory)
    i = 0
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():

            data.ctrl[servo_L] = trajectory[i%n][0] - np.pi/2
            data.ctrl[servo_R] = trajectory[i%n][1] - np.pi/2
            i += 1
            
            mujoco.mj_step(model, data)
            viewer.sync()

if __name__ == "__main__":
    main(5.0)
