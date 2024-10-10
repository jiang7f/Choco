should_print = False

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver
)
from choco.solvers.qiskit.provider.noiseaer import BitFlipNoiseAerProvider, ThermalNoiseAerProvider, DepolarizingNoiseAerProvider,PhaseAmplitudeDampingNoiseAerProvider
import ray

@ray.remote
def get_res_depolar_noise_core(param, problem,problem_scale):
    opt = CobylaOptimizer(max_iter=200)
    aer = DepolarizingNoiseAerProvider(param)
    solver = ChocoSolver(
        prb_model= problem,  # 问题模型
        optimizer=opt,  # 优化器
        provider=aer,  # 提供器（backend + 配对 pass_mannager ）
        num_layers=1,
        shots=1024
        # mcx_mode="linear",
    )
    result = solver.solve()
    scc, incons, ARG, num_bases = solver.evaluation()
    with open('depolar_noise_res.csv', 'a') as f:
        f.write(f'{problem_scale},{param},{scc},{incons},{ARG},{num_bases}\n')

def get_res_depolar_noise_ray(num_case=10, problem_scale_list=[(2, 2)]):
    problems, _ = generate_flp(num_case,problem_scale_list, 1, 100)
    processes = []
        
    with open('depolar_noise_res.csv', 'w') as f:
        f.write('problem_scale,depolar_param,success_rate,inconsistency_rate,ARG,num_bases\n')
    # time unit : ns
    param_lst = [0.001, 0.005, 0.01, 0.03,0.05,0.08,0.1,0.2, 0.5]
    for k in range(len(problem_scale_list)):
        for param in param_lst:
            for i in range(num_case):
                problem = problems[k][i]
                processes.append(get_res_depolar_noise_core.remote(param ,problem,problem_scale_list[k]))
    ray.get(processes)

if __name__ == '__main__':
    get_res_depolar_noise_ray(num_case=100, problem_scale_list=[(2,1),(2, 2),(2,3),(3,1),(3, 2)])


# screen -L -S depolar /home/xdb/miniconda3/envs/qiskit1env310/bin/python /home/xdb/quproj/Choco/test_noise_depolar.py


