import os
import time
import csv
import signal
import random
import itertools
from concurrent.futures import ProcessPoolExecutor, TimeoutError
from choco.problems.facility_location_problem import generate_flp
from choco.problems.graph_coloring_problem import generate_gcp
from choco.problems.k_partition_problem import generate_kpp
from choco.problems.job_scheduling_problem import generate_jsp
from choco.problems.traveling_salesman_problem import generate_tsp
from choco.problems.set_cover_problem import generate_scp
import numpy as np
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

np.random.seed(0x7f)
random.seed(0x7f)

script_path = os.path.abspath(__file__)
new_path = script_path.replace('experiment', 'data')[:-3]

num_cases = 100

flp_problems_pkg, flp_configs_pkg = generate_flp(num_cases, [(1, 2), (3, 2), (3, 3), (3, 4)], 1, 20)
gcp_problems_pkg, gcp_configs_pkg = generate_gcp(num_cases, [(3, 1), (3, 2), (4, 2), (4, 3)])
kpp_problems_pkg, kpp_configs_pkg = generate_kpp(num_cases, [(4, 2, 3), (6, 3, 5), (8, 3, 7), (9, 3, 8)], 1, 20)
jsp_problems_pkg, jsp_configs_pkg = generate_jsp(num_cases, [(2, 2, 3), (3, 3, 5), (3, 4, 6), (4, 5, 7)], 1, 20)
tsp_problems_pkg, tsp_configs_pkg = generate_tsp(num_cases, [4, 5])
scp_problems_pkg, scp_configs_pkg = generate_scp(num_cases, [(4, 8),(8, 15),(12, 20)])


problems_pkg = flp_problems_pkg + gcp_problems_pkg + kpp_problems_pkg + jsp_problems_pkg + tsp_problems_pkg + scp_problems_pkg

configs_pkg = flp_configs_pkg + gcp_configs_pkg + kpp_configs_pkg + jsp_configs_pkg + tsp_configs_pkg + scp_configs_pkg
with open(f"{new_path}.config", "w") as file:
    for pkid, configs in enumerate(configs_pkg):
        for problem in configs:
            file.write(f'{pkid}: {problem}\n')

# mcx_modes = ['constant', 'linear']
metrics_lst = ['depth', 'culled_depth']
solvers = [ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver]
headers = ["pkid", 'method', 'layers'] + metrics_lst

opt = CobylaOptimizer(max_iter=200)
aer = DdsimProvider()
gpu = AerGpuProvider()

def process_layer(prb, num_layers, solver, metrics_lst):
    used_solver = solver(
        prb_model = prb,
        optimizer = opt,
        provider = aer if solver == ChocoSolver else gpu,
        num_layers = num_layers,
        shots = 1024,
    )
    metrics = used_solver.circuit_analyze(metrics_lst)
    return metrics

if __name__ == '__main__':
    set_timeout = 60 * 60 * 24 # Set timeout duration
    num_complete = 0
    script_path = os.path.abspath(__file__)
    new_path = script_path.replace('experiment', 'data')[:-3]
    print(new_path)

    with open(f'{new_path}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers once

        num_processes_cpu = os.cpu_count() // 4
        with ProcessPoolExecutor(max_workers=num_processes_cpu) as executor:
            futures = []
            for solver in solvers:
                for pkid, problems in enumerate(problems_pkg):
                    for problem in problems:
                            if solver == solvers[0]:
                                num_layers = 1
                            else:
                                num_layers = 7
                            future = executor.submit(process_layer, problem, num_layers, solver, metrics_lst)
                            futures.append((future, pkid, solver.__name__, num_layers))

            start_time = time.perf_counter()
            for future, pkid, solver, num_layers in futures:
                current_time = time.perf_counter()
                remaining_time = max(set_timeout - (current_time - start_time), 0)
                diff = []
                try:
                    result = future.result(timeout=remaining_time)
                    diff.extend(result)
                    print(f"Task for problem {pkid}, num_layers {num_layers} executed successfully.")
                except MemoryError:
                    diff.append('memory_error')
                    print(f"Task for problem {pkid}, num_layers {num_layers} encountered a MemoryError.")
                except TimeoutError:
                    diff.append('timeout')
                    print(f"Task for problem {pkid}, num_layers {num_layers} timed out.")
                finally:
                    row = [pkid, solver, num_layers] + diff
                    writer.writerow(row)  # Write row immediately
                    num_complete += 1
                    if num_complete == len(futures):
                        print(f'Data has been written to {new_path}.csv')
                        for process in executor._processes.values():
                            os.kill(process.pid, signal.SIGTERM)