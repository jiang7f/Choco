should_print = True

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver
)
from choco.solvers.qiskit.provider.noiseaer import BitFlipNoiseAerProvider, ThermalNoiseAerProvider, DepolarizingNoiseAerProvider,PhaseAmplitudeDampingNoiseAerProvider
import ray

@ray.remote
def get_res_pauli_error_core(p, problem,problem_scale):
    opt = CobylaOptimizer(max_iter=200)
    aer = BitFlipNoiseAerProvider(p_meas= 1.525e-2, p_reset=p, p_gate1=p)
    solver = ChocoSolver(
        prb_model= problem,  # 问题模型
        optimizer=opt,  # 优化器
        provider=aer,  # 提供器（backend + 配对 pass_mannager ）
        num_layers=3,
        shots=1024
        # mcx_mode="linear",
    )
    result = solver.solve()
    scc, incons, ARG, num_bases = solver.evaluation()
    with open('pauli_error_res.csv', 'a') as f:
        f.write(f'{problem_scale}, {p}, {scc}, {incons}, {ARG}, {num_bases}\n')

def get_res_pauli_error_ray(num_case=10, problem_scale_list=[(2, 2)]):
    problems, _ = generate_flp(num_case,problem_scale_list, 1, 100)
    processes = []
        
    with open('pauli_error_res.csv', 'w') as f:
        f.write('problem_scale,p_gate1,success_rate,incons_rate,ARG,num_bases\n')
    p_gate1_lst = [1e-6,1e-5,5e-5,1e-4,3e-4,5e-4,8e-4,1e-3,1e-2]
    for k in range(len(problem_scale_list)):
        for p in p_gate1_lst:
            for i in range(num_case):
                processes.append(get_res_pauli_error_core.remote(p, problems[k][i], problem_scale_list[k]))
                # processes.append(get_res_pauli_error_core(p, problems[k][i], problem_scale_list[k]))
    ray.get(processes)

if __name__ == '__main__':
    get_res_pauli_error_ray(num_case=100, problem_scale_list=[(2, 1),(2, 2),(2,3),(3,1),(3, 2)])


#  screen -L -S pauli /home/xdb/miniconda3/envs/qiskit1env310/bin/python /home/xdb/quproj/Choco/test_noise.py

