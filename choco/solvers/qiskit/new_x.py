import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

from choco.solvers.abstract_solver import Solver
from choco.solvers.optimizers import Optimizer
from choco.solvers.options import CircuitOption, OptimizerOption, ModelOption
from choco.solvers.options.circuit_option import ChCircuitOption
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.utils import iprint

from .circuit import QiskitCircuit
from .provider import Provider
from .circuit.circuit_components import obj_compnt, new_x_compnt


class NewXCircuit(QiskitCircuit[ChCircuitOption]):
    def __init__(self, circuit_option: ChCircuitOption, model_option: ModelOption):
        super().__init__(circuit_option, model_option)
        # self.model_option.Hd_bitstr_list = list(reversed(self.model_option.Hd_bitstr_list))
        # self.model_option.feasible_state = [0, 0, 1, 0, 0]
        first_row = self.model_option.Hd_bitstr_list[0, :]
        self.model_option.Hd_bitstr_list = np.vstack([self.model_option.Hd_bitstr_list, first_row])

        iprint(self.model_option.feasible_state)
        iprint(self.model_option.Hd_bitstr_list)

        self.inference_circuit = self.create_circuit()

    def get_num_params(self):
        return self.model_option.num_qubits
    
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
            qc = QuantumCircuit(num_qubits, num_qubits)
            # anc_idx = [num_qubits, num_qubits + 1]
        elif mcx_mode == "linear":
            qc = QuantumCircuit(num_qubits, num_qubits)
            # anc_idx = list(range(num_qubits, 2 * num_qubits))

        num_bitstrs = len(self.model_option.Hd_bitstr_list)
        Hd_params_lst = [Parameter(f"Hd_params[{j}]") for j in range(num_qubits)]

        # for i in np.nonzero(self.model_option.feasible_state)[0]:
        #     qc.x(i)

        # for layer in range(num_layers):
            # new_x_compnt(
            #     qc,
            #     Hd_params_lst[layer],
            #     self.model_option.Hd_bitstr_list,
            # )
        print(len(Hd_params_lst))
        for i in range(num_qubits):
            qc.rx(Hd_params_lst[i], i)

        qc.measure(range(num_qubits), range(num_qubits)[::-1])
        transpiled_qc = self.circuit_option.provider.transpile(qc)
        return transpiled_qc

class NewXSolver(Solver):
    def __init__(
        self,
        *,
        prb_model: LcboModel,
        optimizer: Optimizer,
        provider: Provider,
        num_layers: int = 1,
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
            self._circuit = NewXCircuit(self.circuit_option, self.model_option)
        return self._circuit


