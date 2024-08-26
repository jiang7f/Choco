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


class PenaltyCircuit(QiskitCircuit[CircuitOption]):
    def __init__(self, circuit_option: CircuitOption, model_option: ModelOption):
        super().__init__(circuit_option, model_option)
        self.inference_circuit = self.create_circuit()

    def get_num_params(self):
        return self.circuit_option.num_layers * 2
    
    def inference(self, params):
        final_qc = self.inference_circuit.assign_parameters(params)
        counts = self.circuit_option.provider.get_counts(final_qc, shots=self.circuit_option.shots)
        collapse_state, probs = self.process_counts(counts)
        return collapse_state, probs

    def create_circuit(self) -> QuantumCircuit:
        num_layers = self.circuit_option.num_layers
        num_qubits = self.model_option.num_qubits

        qc = QuantumCircuit(num_qubits, num_qubits)
        Ho_params = [Parameter(f'Ho_params[{i}]') for i in range(num_layers)]
        Hd_params = [Parameter(f'Hd_params[{i}]') for i in range(num_layers)]
        
        for i in range(num_qubits):
            qc.h(i)

        for layer in range(num_layers):
            obj_compnt(qc, Ho_params[layer], self.model_option.obj_dct)

            for i in range(num_qubits):
                qc.rx(Hd_params[layer], i)

        qc.measure(range(num_qubits), range(num_qubits)[::-1])
        transpiled_qc = self.circuit_option.provider.pass_manager.run(qc)
        return transpiled_qc
    
class PenaltySolver(Solver):
    def __init__(
        self,
        *,
        prb_model: LcboModel,
        optimizer: Optimizer,
        provider: Provider,
        num_layers: int,
        shots: int = 1024,
    ):
        super().__init__(prb_model, optimizer)
        self.circuit_option = CircuitOption(
            provider=provider,
            num_layers=num_layers,
            shots=shots,
        )

    @property
    def circuit(self):
        if self._circuit is None:
            self._circuit = PenaltyCircuit(self.circuit_option, self.mode_option)
        return self._circuit