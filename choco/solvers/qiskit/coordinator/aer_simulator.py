from .coordinator import Coordinator
from qiskit import QuantumCircuit

class AerSimulator(Coordinator):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.pass_manager = None

    def get_counts(self, qc: QuantumCircuit):
        pass


class AerSimulatorGpu(Coordinator):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.pass_manager = None

    def get_counts(self, qc: QuantumCircuit):
        pass
