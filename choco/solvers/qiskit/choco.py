from ..abstract_solver import Solver
from ..optimizers import Optimizer
from .circuit import QiskitCircuit
from ..options import ChocoCircuitOption, OptimizerOption
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np
from .circuit.circuit_components import obj_compnt, commute_compnt
from mqt import ddsim


class ChocoCircuit(QiskitCircuit[ChocoCircuitOption]):
    def __init__(self, circuit_option: ChocoCircuitOption):
        super().__init__(circuit_option)
        self.inference_circuit = self.create_circuit()

    def inference(self, params):
        counts = {}
        final_qc = self.inference_circuit.assign_parameters(params)
        job = self.circuit_option.backend.run(final_qc, shots=self.circuit_option.shots)
        counts = job.result().get_counts(final_qc)

        collapse_state, probs = self.process_counts(counts)
        return collapse_state, probs


    def create_circuit(self):
        mcx_mode = self.circuit_option.mcx_mode
        num_qubits = self.circuit_option.num_qubits
        num_layers = self.circuit_option.num_layers
        if mcx_mode == "constant":
            qc = QuantumCircuit(num_qubits + 2, num_qubits)
            anc_idx = [num_qubits, num_qubits + 1]
        elif mcx_mode == "linear":
            qc = QuantumCircuit(2 * num_qubits, num_qubits)
            anc_idx = list(range(num_qubits, 2 * num_qubits))

        Ho_params = [Parameter(f"Ho_params[{i}]") for i in range(num_layers)]
        Hd_params = [Parameter(f"Hd_params[{i}]") for i in range(num_layers)]

        assert len(Hd_params) == num_layers
        for i in np.nonzero(self.circuit_option.feasible_state)[0]:
            qc.x(i)

        for layer in range(num_layers):
            obj_compnt(qc, Ho_params[layer], self.circuit_option.obj_dct)
            commute_compnt(qc, Hd_params[layer], self.circuit_option.Hd_bitstr_list, anc_idx, mcx_mode)

        qc.measure(range(num_qubits), range(num_qubits)[::-1])
        transpiled_qc = self.circuit_option.pass_manager.run(qc)
        return transpiled_qc

class ChocoSolver(Solver):
    def __init__(
        self,
        num_layers,
        backend,
        mcx_mode,
        optimizer: Optimizer,
    ):
        self.circuit_option = ChocoCircuitOption(
            num_layers=num_layers,
            backend=backend,
            mcx_mode=mcx_mode,
        )