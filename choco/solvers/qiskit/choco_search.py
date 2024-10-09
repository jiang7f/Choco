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
from .circuit.circuit_components import obj_compnt, commute_search_evolution_space


class ChocoCircuitSearch(QiskitCircuit[ChCircuitOption]):
    def __init__(self, circuit_option: ChCircuitOption, model_option: ModelOption):
        super().__init__(circuit_option, model_option)
        self.result = self.create_circuit()

    def get_num_params(self):
        return self.circuit_option.num_layers * 2
    
    def inference(self, params):
        print("use func: search")
        exit()

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
        Hd_params = np.full(num_layers, np.pi/4)
        # Hd_params = np.random.rand(num_layers)

        for i in np.nonzero(self.model_option.feasible_state)[0]:
            qc.x(i)
        num_basis_list = []
        depth_lists = []
        for layer in range(num_layers):
            print(f"===== Layer:{layer + 1} ======")
            obj_compnt(qc, Ho_params[layer], self.model_option.obj_dct)
            # order=[7, 0, 6,8,5,4,3,2,1]
            # new_order = sorted_list = [self.model_option.Hd_bitstr_list[i] for i in order]
            basis_list, depth_list = commute_search_evolution_space(
                qc,
                Hd_params[layer],
                # new_order,
                self.model_option.Hd_bitstr_list,
                anc_idx,
                mcx_mode,
                num_qubits,
                self.circuit_option.shots
            )
            num_basis_list.extend(basis_list)
            depth_lists.extend(depth_list)
        return num_basis_list, depth_lists


class ChocoSolverSearch(Solver):
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
            self._circuit = ChocoCircuitSearch(self.circuit_option, self.model_option)
        return self._circuit

    def search(self):
        return self.circuit.result
