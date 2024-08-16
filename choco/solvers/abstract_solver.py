from abc import ABC, abstractmethod
from .option import CircuitOption, OptimizerOption
from ..model import lin_constr_bin_opt

class Solver(ABC):
    def __init__(self, circuit_option: CircuitOption, optimizer_option: OptimizerOption):
        self.circuit_option = circuit_option
        self.optimizer_option = optimizer_option
    
    
    def model_load(self, prb_model: lin_constr_bin_opt):
        pass

    @abstractmethod
    def abc():
        pass

