import mujoco
import mujoco.viewer
import numpy as np

model = mujoco.MjModel.from_xml_path("five_bar.xml")
data = mujoco.MjData(model)

servo_L = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_L")
servo_R = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_R")

def main(n):
    with mujoco.viewer.launch_passive(model, data) as viewer:
        while viewer.is_running():
            target_pos = np.sin(data.time/50)

            data.ctrl[servo_L] = target_pos
            data.ctrl[servo_R] = -1 * target_pos

            mujoco.mj_step(model, data)
            viewer.sync()

if __name__ == "__main__":
    main(5.0)
