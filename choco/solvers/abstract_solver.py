from abc import ABC, abstractmethod
from .options import CircuitOption
from ..solvers.optimizers import Optimizer
from ..utils import iprint
from ..model import LinearConstrainedBinaryOptimization as LcboModel
from .options.model_option import ModelOption
from .qiskit.provider import Provider
from dataclasses import replace, asdict
from .qiskit.circuit import QiskitCircuit
from .data_analyzer import DataAnalyzer

class Solver(ABC):
    def __init__(self, prb_model: LcboModel, optimizer: Optimizer):
        self.mode_option: ModelOption = prb_model.to_model_option()
        self.optimizer: Optimizer = optimizer
        self.circuit_option: CircuitOption = None

        self._circuit = None

        self.collapse_state_lst = None
        self.probs_lst = None
        self.iter_count = None
        self.evaluation_lst = None

    # def load_model(self, model_option: ModelOption):
    #     self.model_option = model_option
    #     iprint(f"fsb_state: {self.model_option.feasible_state}")  # -
    #     iprint(f"driver_bit_stirng:\n {self.model_option.Hd_bitstr_list}")  # -

    @property
    @abstractmethod
    def circuit(self) -> QiskitCircuit:
        pass

    def solve(self):
        self.optimizer.optimizer_option.cost_func = self.circuit.get_circuit_cost_func()
        self.optimizer.optimizer_option.num_params = self.circuit.get_num_params()
        best_params, self.iter_count = self.optimizer.minimize()
        self.collapse_state_lst, self.probs_lst = self.circuit.inference(best_params)
        return self.collapse_state_lst, self.probs_lst, self.iter_count
    
    def evaluation(self):
        '''在调用过solve之后使用'''
        assert self.collapse_state_lst is not None

        mode_option = self.mode_option
        data_analyzer = DataAnalyzer(
            self.collapse_state_lst, 
            self.probs_lst, 
            mode_option.obj_func, 
            mode_option.obj_dir, 
            mode_option.best_cost,
            mode_option.lin_constr_mtx
        )
        data_metrics_lst = data_analyzer.summary()
        # 把 iteration_count 加到 指标 结尾，构成完整评估
        self.evaluation_lst = data_metrics_lst + [self.iter_count]
        return self.evaluation_lst
        

    # def __hash__(self):
    #     # 使用一个元组的哈希值作为对象的哈希值
    #     return hash(self.name)

    # def __eq__(self, other):
    #     if isinstance(other, Solver):
    #         return self.name == other.name
    #     return False
