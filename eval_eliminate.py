# should_print = True
import os
import time
import csv
import signal
import random
import itertools
from concurrent.futures import ProcessPoolExecutor, TimeoutError
import numpy as np
from choco.solvers.abstract_solver import Solver
from choco.problems.facility_location_problem import generate_flp
from choco.problems.graph_coloring_problem import generate_gcp
from choco.problems.k_partition_problem import generate_kpp
from choco.problems.job_scheduling_problem import generate_jsp
from choco.problems.traveling_salesman_problem import generate_tsp
from choco.problems.set_cover_problem import generate_scp
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)
from choco.solvers.technology.eliminate import Eliminate_variables

np.random.seed(0x7f)

script_path = os.path.abspath(__file__)
new_path = script_path.replace('experiment', 'data')[:-3]

num_cases = 200

flp_problems_pkg, flp_configs_pkg = generate_flp(num_cases, [(1, 2), (3, 2), (3, 3), (3, 4)], 1, 20)
gcp_problems_pkg, gcp_configs_pkg = generate_gcp(num_cases, [(3, 1), (3, 2), (4, 2), (4, 3)])
kpp_problems_pkg, kpp_configs_pkg = generate_kpp(num_cases, [(4, 2, 3), (6, 3, 5), (8, 3, 7), (9, 3, 8)], 1, 20)
jsp_problems_pkg, jsp_configs_pkg = generate_jsp(num_cases, [(2, 2, 3), (3, 3, 5), (3, 4, 6), (4, 5, 7)], 1, 20)
tsp_problems_pkg, tsp_configs_pkg = generate_tsp(num_cases, [4, 5])
scp_problems_pkg, scp_configs_pkg = generate_scp(num_cases, [(4, 8),(8, 15),(12, 20)])


# problems_pkg = flp_problems_pkg + gcp_problems_pkg + kpp_problems_pkg + jsp_problems_pkg + tsp_problems_pkg + scp_problems_pkg
problems_pkg = list(itertools.chain(enumerate(flp_problems_pkg), enumerate(gcp_problems_pkg), enumerate(kpp_problems_pkg), enumerate(jsp_problems_pkg), enumerate(tsp_problems_pkg), enumerate(scp_problems_pkg)))
configs_pkg = flp_configs_pkg + gcp_configs_pkg + kpp_configs_pkg + jsp_configs_pkg + tsp_configs_pkg + scp_configs_pkg

with open(f"{new_path}.config", "w") as file:
    for pkid, configs in enumerate(configs_pkg):
        for pbid, problem in enumerate(configs):
            file.write(f'{pkid}-{pbid}: {problem}\n')


solvers = [ChocoSolver]
evaluation_metrics = ['best_solution_probs']
headers = ['pkid', 'pbid', 'layers', "variables", 'constraints', 'method'] + evaluation_metrics

opt = CobylaOptimizer(max_iter=1000)
aer = DdsimProvider()

def process_layer(prb, num_layers, solver: Solver):
    e_solver = Eliminate_variables(
        solver = solver,
        prb_model = prb,
        optimizer = opt,
        provider = aer,
        num_layers = num_layers,
        shots = 1024,
        num_frozen_qubit=1,
    )
    e_solver.solve()
    eval = e_solver.evaluation()
    return eval

if __name__ == '__main__':
    all_start_time = time.perf_counter()
    set_timeout = 60 * 60 * 24 * 3 # Set timeout duration
    num_complete = 0
    print(new_path)
    with open(f'{new_path}.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)  # Write headers once

        num_processes_cpu = os.cpu_count()
        # pkid-pbid: 问题包序-包内序号
        for pkid, (diff_level, problems) in enumerate(problems_pkg):
            for solver in solvers:
                if solver == 'commute':
                    num_processes = num_processes_cpu // 2
                else:
                    num_processes = 2**(4 - diff_level)
                with ProcessPoolExecutor(max_workers=num_processes) as executor:
                    futures = []
                    if solver == solvers[0]:
                        layer = 1
                    else:
                        layer = 7
                    for pbid, prb in enumerate(problems):
                        print(f'{pkid}-{pbid}, {layer}, {solver} build')
                        future = executor.submit(process_layer, prb, layer, solver)
                        futures.append((future, prb, pkid, pbid, layer, solver.__name__))

                    start_time = time.perf_counter()
                    for future, prb, pkid, pbid, layer, solver in futures:
                        current_time = time.perf_counter()
                        remaining_time = max(set_timeout - (current_time - start_time), 0)
                        diff = []
                        try:
                            metrics = future.result(timeout=remaining_time)
                            diff.append(metrics)
                            print(f"Task for problem {pkid}-{pbid} L={layer} {solver} executed successfully.")
                        except MemoryError:
                            print(f"Task for problem {pkid}-{pbid} L={layer} {solver} encountered a MemoryError.")
                            for dict_term in evaluation_metrics:
                                diff.append('memory_error')
                        except TimeoutError:
                            print(f"Task for problem {pkid}-{pbid} L={layer} {solver} timed out.")
                            for dict_term in evaluation_metrics:
                                diff.append('timeout')
                        except Exception as e:
                            print(f"An error occurred: {e}")
                        finally:
                            row = [pkid, pbid, layer, len(prb.variables), len(prb.lin_constr_mtx), solver] + diff
                            writer.writerow(row)  # Write row immediately
                            num_complete += 1
                            if num_complete == len(futures):
                                print(f'problem_pkg_{pkid} has finished')
                                for process in executor._processes.values():
                                    os.kill(process.pid, signal.SIGTERM)
    print(f'Data has been written to {new_path}.csv')
    print(time.perf_counter()- all_start_time)