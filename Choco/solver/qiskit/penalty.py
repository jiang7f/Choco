from .solver import Solver
from ..option import CircuitOption, OptimizerOption

class PenaltySolver(Solver):
    def __init__(self, circuit_option: CircuitOption, optimizer_option: OptimizerOption):
        super().__init__(circuit_option, optimizer_option)