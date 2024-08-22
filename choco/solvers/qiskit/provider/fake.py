from .provider import Provider
from qiskit import QuantumCircuit

class FakeKyivProvider(Provider):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.pass_manager = None

    def get_counts(self, qc: QuantumCircuit):
        pass

class FakeTorinoProvider(Provider):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.pass_manager = None

    def get_counts(self, qc: QuantumCircuit):
        pass

class FakeBrisbaneProvider(Provider):
    def __init__(self):
        super().__init__()
        self.backend = None
        self.pass_manager = None

    def get_counts(self, qc: QuantumCircuit):
        pass