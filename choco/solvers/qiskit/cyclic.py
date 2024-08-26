import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from choco.solvers.abstract_solver import Solver
from choco.solvers.optimizers import Optimizer
from choco.solvers.options import CircuitOption, OptimizerOption, ModelOption
from choco.solvers.options.circuit_option import ChocoCircuitOption
from choco.model import LinearConstrainedBinaryOptimization as LcboModel

from .circuit import QiskitCircuit
from .provider import Provider
from .circuit.circuit_components import obj_compnt, commute_compnt


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

class CyclicSolver(Solver):
    def __init__(self, circuit_option: CircuitOption, optimizer_option: OptimizerOption):
        super().__init__(circuit_option, optimizer_option)