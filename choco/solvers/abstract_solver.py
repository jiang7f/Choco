from abc import ABC, abstractmethod
from .options import CircuitOption
from ..solvers.optimizers import Optimizer
from ..utils import iprint
from .qiskit.coordinator import Coordinator


class Solver(ABC):
    def __init__(self, num_layers: int, coordinator: Coordinator, optimizer: Optimizer):
        self.circuit_option = self.create_circuit_option(num_layers, coordinator)
        self.optimizer: Optimizer = optimizer

    @abstractmethod
    def create_circuit_option(self, num_layers: int, coordinator: Coordinator) -> CircuitOption:
        pass


    @abstractmethod
    def build_circuit(self):
        pass

    def circuit_analyze(self, feedback):
        pass

    def solve(self):
        self.optimizer.minimize()
        return 1, 2, 3

    # def __hash__(self):
    #     # 使用一个元组的哈希值作为对象的哈希值
    #     return hash(self.name)

    # def __eq__(self, other):
    #     if isinstance(other, Solver):
    #         return self.name == other.name
    #     return False
