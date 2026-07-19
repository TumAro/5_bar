import mujoco
import mujoco.viewer
import numpy as np
import numpy as np
from test import circle_trajectory
from src import ILC
from src.utils import u2theta, theta2u, read_state, plot

model = mujoco.MjModel.from_xml_path("five_bar.xml")
data = mujoco.MjData(model)

servo_L = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_L")
servo_R = mujoco.mj_name2id(model, mujoco.mjtObj.mjOBJ_ACTUATOR, "servo_R")

def ilc_convergence(trials : int = 10):
    trajectory = circle_trajectory()
    controller = ILC(u0 = trajectory)
    error_norms = []

    for trial in range(trials):
        mujoco.mj_resetData(model, data)

        actual_trial = []
        for i, wp in enumerate(trajectory):
            data.ctrl[servo_L], data.ctrl[servo_R] = u2theta(controller.u[i])
            mujoco.mj_step(model, data)
            actual_trial.append(theta2u(read_state(model, data)))

        controller.step(np.array(actual_trial), np.array(trajectory))
        error_norms.append(controller.error_norms[-1])
        print(f"Trial {trial+1} : error norm -> {controller.error_norms[-1]}")

    return controller, error_norms, trajectory

def main():
    controller, error_norms, trajectory = ilc_convergence(trials=52)
    plot(error_norms, title="ILC convergence", xlabel="trial", ylabel="error norm")


if __name__ == "__main__":
    main()
