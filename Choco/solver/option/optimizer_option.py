from dataclasses import dataclass, field
from typing import List, Callable, Tuple

@dataclass
class OptimizerOption:
    params_optimization_method: str = 'COBYLA'
    max_iter: int = 30
    learning_rate: float = 0.1
    beta1: float = 0.9
    beta2: float = 0.999
    opt_id: any = None
    use_local_params: bool = False
    #
    circuit_cost_function: Callable = None
    num_params: int = None