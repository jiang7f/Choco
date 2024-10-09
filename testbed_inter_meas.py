should_print = False

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, ChocoInterMeasSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider, SimulatorProvider
)

num_case = 100
prbs = [(1, 2), (2, 3)]
a, b = generate_flp(num_case, prbs, 1, 100)
# print(a[0][0])
# (1, [(2, 1), (3, 2), (3, 3), (4, 3), (4, 4)], 1, 20)

best_lst = []
in_cnst_list = []
arg_lst = []
iter_lst = []

import os
import csv
script_path = os.path.abspath(__file__)
new_path = script_path.replace('experiment', 'data')[:-3]
headers = ["pkid", "solverid", "success", "incnstr", "arg", "iter"]
with open(f'{new_path}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers once


solvers = [ChocoInterMeasSolver, ChocoSolver]
for prb in range(len(prbs)):
    for solver_id in range(len(solvers)):
        for i in range(num_case):
            opt = CobylaOptimizer(max_iter=200)
            aer = SimulatorProvider()
            solver = solvers[solver_id](
                prb_model=a[prb][i],  # 问题模型
                optimizer=opt,  # 优化器
                provider=aer,  # 提供器（backend + 配对 pass_mannager ）
                num_layers=1,
                shots=1024
                # mcx_mode="linear",
            )

            result = solver.solve()
            u, v, w, x = solver.evaluation()
            print(f"{i}: {u}, {v}, {w}, {x}")
            best_lst.append(u)
            in_cnst_list.append(v)
            arg_lst.append(w)
            iter_lst.append(x)
        with open(f'{new_path}.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([prb, solver_id, sum(best_lst) / num_case, sum(in_cnst_list) / num_case, sum(arg_lst) / num_case, sum(iter_lst) / num_case])
        print(sum(best_lst) / num_case, sum(in_cnst_list) / num_case, sum(arg_lst) / num_case, sum(iter_lst) / num_case)
