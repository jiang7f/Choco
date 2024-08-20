from abc import ABC, abstractmethod
from .options import CircuitOption
from ..model import LinearConstrainedBinaryOptimization as LcboModel
from ..solvers.optimizers import Optimizer
from ..utils import iprint


class Solver(ABC):
    def __init__(self, num_layers, backend, pass_manager, optimizer: Optimizer):
        self.circuit_option = CircuitOption(
            num_layers=num_layers, backend=backend, pass_manager=pass_manager
        )
        self.optimizer: Optimizer = optimizer

    def model_load(self, prb_model: LcboModel):
        circuit_option = self.circuit_option
        circuit_option.num_qubits = len(prb_model.variables)
        circuit_option.penalty_lambda = prb_model.penalty_lambda
        circuit_option.feasible_state = prb_model.get_feasible_solution()
        circuit_option.obj_dct = prb_model.obj_dct
        circuit_option.lin_constr_mtx = prb_model.lin_constr_mtx
        circuit_option.Hd_bitstr_list = prb_model.driver_bitstr
        circuit_option.obj_func = prb_model.obj_func
        iprint(f"fsb_state: {circuit_option.feasible_state}")  # -
        iprint(f"driver_bit_stirng:\n {circuit_option.Hd_bitstr_list}")  # -

    @abstractmethod
    def build_circuit(self):
        pass

    def circuit_analyze(self, feedback):
        pass

    def solve(self):
        self.optimizer.minimize()
        return 1, 2, 3

    # def __hash__(self):
    #     # 使用一个元组的哈希值作为对象的哈希值
    #     return hash(self.name)

    # def __eq__(self, other):
    #     if isinstance(other, Solver):
    #         return self.name == other.name
    #     return False
