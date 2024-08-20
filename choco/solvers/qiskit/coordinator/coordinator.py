from abc import ABC, abstractmethod
from typing import Dict, Union, Callable
from qiskit import QuantumCircuit
from qiskit.providers import Backend, BackendV2
from qiskit.transpiler import PassManager


class Coordinator(ABC):
    def __init__(self):
        self.backend = None
        self.pass_manager = None

    @abstractmethod
    def get_counts(self, qc: QuantumCircuit) -> Dict:
        pass


class CustomCoordinator(Coordinator):
    def __init__(
        self,
        backend: Union[Backend, BackendV2],
        pass_manager: PassManager,
        get_counts_fun: Callable[[QuantumCircuit], dict]
    ):
        self.backend = backend
        self.pass_manager = pass_manager
        self.get_counts = get_counts_fun
