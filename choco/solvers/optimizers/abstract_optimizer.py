from ...solvers.options import OptimizerOption
import numpy as np

# np.random.seed(0x7f)

class Optimizer:
    def __init__(self, optimizer_option: OptimizerOption):
        self.params = 2 * np.pi * np.random.uniform(0, 1, optimizer_option.num_params)

    def minimize(self):
        pass