import numpy as np

class ILC:
    def __init__(self, u0: np.ndarray, gain: float = 0.2):
        """
            u0: starting commanded trajectory - [theta1, theta2]
            gain: %age of error per trial
        """
        self.u = u0.copy()
        self.g = gain
        self.error_norms = []

    def step(self, actual: np.ndarray, desired: np.ndarray) -> None:
        """call after each trial. Returns next u to run"""
        e = desired - actual
        self.error_norms.append(np.linalg.norm(e))
        self.u = self.u + self.g * e    # * u gets mutated in each call
