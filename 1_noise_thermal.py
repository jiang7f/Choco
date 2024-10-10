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
def get_res_Thermal_noise_core(t1,t2, problem,problem_scale):
    opt = CobylaOptimizer(max_iter=200)
    aer = ThermalNoiseAerProvider(t1=t1, t2=t2)
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
    with open('thermal_noise_res.csv', 'a') as f:
        f.write(f'{problem_scale},{t1},{t2},{scc},{incons},{ARG},{num_bases}\n')

def get_res_Thermal_noise_ray(num_case=10, problem_scale_list=[(2, 2)]):
    problems, _ = generate_flp(num_case,problem_scale_list, 1, 100)
    processes = []
        
    with open('thermal_noise_res.csv', 'w') as f:
        f.write('problem_scale,t1,t2,success_rate,inconsistency_rate,ARG,num_bases\n')
    # time unit : ns
    t1_lst = [100, 1000, 10000, 100000,500000, 1000000, 5000000, 10000000]
    t2_scale_list = [1.1,1.3,1.5,1.8,1.9,2]
    for k in range(len(problem_scale_list)):
        for t in t1_lst:
            for t2_scale in t2_scale_list:
                t2 = t * t2_scale
                for i in range(num_case):
                    problem = problems[k][i]
                    processes.append(get_res_Thermal_noise_core.remote(t,t2, problem,problem_scale_list[k]))
    ray.get(processes)

if __name__ == '__main__':
    get_res_Thermal_noise_ray(num_case=10, problem_scale_list=[(2,1),(2, 2),(2,3),(3,1),(3, 2)])

# screen -L -S thermal /home/xdb/miniconda3/envs/qiskit1env310/bin/python /home/xdb/quproj/Choco/test_noise_thermal.py
