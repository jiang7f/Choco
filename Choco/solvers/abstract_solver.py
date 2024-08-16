from abc import ABC, abstractmethod
from .option import CircuitOption, OptimizerOption
class Solver(ABC):
    def __init__(self, circuit_option: CircuitOption, optimizer_option: OptimizerOption):
        self.circuit_option = circuit_option
        self.optimizer_option = optimizer_option

    @abstractmethod
    def abc():
        pass

