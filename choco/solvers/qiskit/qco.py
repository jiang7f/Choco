from ..abstract_solver import Solver
from .circuit import QiskitCircuit
from ..options import CircuitOption, OptimizerOption


class ChocoCircuit(QiskitCircuit):
    def __init__(self, circuit_option: CircuitOption):
        super().__init__(circuit_option)

    def inference(self, params):
        counts = {}
        final_qc = self.inference_circuit
        self.process_counts(counts)
        pass

    def create_circuit(self) -> None:
        pass

class QcoSolver(Solver):
    def __init__(self, circuit_option: CircuitOption, optimizer_option: OptimizerOption):
        super().__init__(circuit_option, optimizer_option)