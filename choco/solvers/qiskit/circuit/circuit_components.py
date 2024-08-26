import numpy as np
from itertools import combinations
from qiskit import QuantumCircuit
from typing import Dict
from .hdi_decompose import driver_component


def obj_compnt(qc: QuantumCircuit, param, obj_dct: Dict):
    """https://quantumcomputing.stackexchange.com/questions/5567/circuit-construction-for-hamiltonian-simulation"""

    for pow, terms in obj_dct.items():
        for vars_tuple, coeff in terms:
            for k in range(1, pow + 1):
                fianl_theta = (1 / 2) ** pow * 2 * coeff * (-1) ** k
                for combo in combinations(range(pow), k):
                    for i in range(len(combo) - 1):
                        qc.cx(vars_tuple[combo[i]], vars_tuple[combo[i + 1]])
                    qc.rz(fianl_theta * param, vars_tuple[combo[-1]])
                    for i in range(len(combo) - 2, -1, -1):
                        qc.cx(vars_tuple[combo[i]], vars_tuple[combo[i + 1]])


def commute_compnt(qc: QuantumCircuit, param, Hd_bitstr_list, anc_idx, mcx_mode):
    for hdi_vct in Hd_bitstr_list:
        nonzero_indices = np.nonzero(hdi_vct)[0].tolist()
        hdi_bitstr = [0 if x == -1 else 1 for x in hdi_vct if x != 0]
        driver_component(qc, nonzero_indices, anc_idx, hdi_bitstr, param, mcx_mode)
