from abc import ABC, abstractmethod
from ...solvers.options import OptimizerOption
from typing import TypeVar, Generic
import numpy as np

# np.random.seed(0x7f)

class Optimizer(ABC):
    def __init__(self):
        self.optimizer_option: OptimizerOption = None

    @abstractmethod
    def minimize(self):
        pass

    def _initialize_params(self, num_params):
        """初始化电路参数"""
        return 2 * np.pi * np.random.uniform(0, 1, num_params)