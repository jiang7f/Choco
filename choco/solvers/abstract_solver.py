from abc import ABC, abstractmethod
from .options import CircuitOption, OptimizerOption
from ..model import LinearConstrainedBinaryOptimization as LcboModel
from ..solvers.optimizers import Optimizer

class Solver(ABC):
    def __init__(self, circuit_option: CircuitOption, optimizer: Optimizer):
        self.circuit_option = circuit_option
        self.optimizer = optimizer

        # self.
    
    
    def model_load(self, prb_model: LcboModel):
        self.circuit_option.num_qubits = len(prb_model.variables)
        pass

    @abstractmethod
    def optimize(self):
        pass
        return 1, 2, 3



    @abstractmethod
    def abc():
        pass

