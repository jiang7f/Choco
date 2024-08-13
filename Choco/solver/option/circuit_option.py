from dataclasses import dataclass, field
from typing import List, Callable, Tuple

@dataclass
class CircuitOption:
    num_layers: int = 2
    need_draw: bool = False
    use_decompose: bool = False
    use_serialization : bool = False # 不分解情况的可选项
    circuit_type: str = 'qiskit'
    mcx_mode: str = 'constant'  # 'constant' for 2 additional ancillas with linear depth, 'linear' for n-1 additional ancillas with logarithmic depth
    backend: str = 'FakeAlmadenV2' #'FakeQuebec' # 'AerSimulator'\
    feedback: List = field(default_factory=list)
    shots: int = 1024
    use_IBM_service_mode: str = None
    use_free_IBM_service: bool = True
    use_fake_IBM_service: bool = False
    cloud_manager: CloudManager = None
    # 
    # log_depth: bool = False
    num_qubits: int = 0
    algorithm_optimization_method: str = 'commute'
    penalty_lambda: float = None
    objective_func: Callable = None
    feasiable_state: List[int] = field(default_factory=list)
    objective_func_term_list: List[List[Tuple[List[int], float]]] = field(default_factory=list)
    linear_constraints: List[List[float]] = field(default_factory=list)
    constraints_for_cyclic: List[List[float]] = field(default_factory=list)
    constraints_for_others: List[List[float]] = field(default_factory=list)
    Hd_bits_list: List[List[int]] = field(default_factory=list)