import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from choco.solvers.abstract_solver import Solver
from choco.solvers.optimizers import Optimizer
from choco.solvers.options import CircuitOption, OptimizerOption, ModelOption
from choco.solvers.options.circuit_option import ChCircuitOption
from choco.model import LinearConstrainedBinaryOptimization as LcboModel

from .circuit import QiskitCircuit
from .provider import Provider
from .circuit.circuit_components import obj_compnt, commute_compnt_for_mid


class ChocoCircuitMid(QiskitCircuit[ChCircuitOption]):
    def __init__(self, circuit_option: ChCircuitOption, model_option: ModelOption):
        super().__init__(circuit_option, model_option)
        self.inference_circuit = self.create_circuit()
        print(self.model_option.Hd_bitstr_list)

    def get_num_params(self):
        return self.circuit_option.num_layers * 2
    
    def inference(self, params):
        final_qc = self.inference_circuit.assign_parameters(params)
        counts = self.circuit_option.provider.get_counts(final_qc, shots=self.circuit_option.shots)
        collapse_state, probs = self.process_counts(counts)
        return collapse_state, probs

    def create_circuit(self) -> QuantumCircuit:
        mcx_mode = self.circuit_option.mcx_mode
        num_layers = self.circuit_option.num_layers
        num_qubits = self.model_option.num_qubits
        if mcx_mode == "constant":
            qc = QuantumCircuit(num_qubits + 2, num_qubits)
            anc_idx = [num_qubits, num_qubits + 1]
        elif mcx_mode == "linear":
            qc = QuantumCircuit(2 * num_qubits, num_qubits)
            anc_idx = list(range(num_qubits, 2 * num_qubits))

        Ho_params = np.random.rand(num_layers)
        # Hd_params = np.full(num_layers, np.pi/4)
        Hd_params = np.random.rand(num_layers)

        for i in np.nonzero(self.model_option.feasible_state)[0]:
            qc.x(i)

        for layer in range(num_layers):
            print(f"===== Layer:{layer + 1} ======")
            obj_compnt(qc, Ho_params[layer], self.model_option.obj_dct)
            commute_compnt_for_mid(
                qc,
                Hd_params[layer],
                self.model_option.Hd_bitstr_list,
                anc_idx,
                mcx_mode,
                num_qubits,
            )
            
        exit()
        qc.measure(range(num_qubits), range(num_qubits)[::-1])
        transpiled_qc = self.circuit_option.provider.pass_manager.run(qc)
        print(transpiled_qc.draw())
        return transpiled_qc

class ChocoSolverMid(Solver):
    def __init__(
        self,
        *,
        prb_model: LcboModel,
        optimizer: Optimizer,
        provider: Provider,
        num_layers: int,
        shots: int = 1024,
        mcx_mode: str = "linear",
    ):
        super().__init__(prb_model, optimizer)
        self.circuit_option = ChCircuitOption(
            provider=provider,
            num_layers=num_layers,
            shots=shots,
            mcx_mode=mcx_mode,
        )

    @property
    def circuit(self):
        if self._circuit is None:
            self._circuit = ChocoCircuitMid(self.circuit_option, self.mode_option)
        return self._circuit


