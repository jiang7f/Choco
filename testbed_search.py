should_print = True

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, ChocoSolverSearch, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 1
prbs = [(1, 2), (2, 3), (3, 3), (3, 4)]
a, b = generate_flp(num_case, prbs, 1, 100)
print(a[3][0].calculate_feasible_solution())
exit()

best_lst = []
arg_lst = []

import os
import csv
script_path = os.path.abspath(__file__)
new_path = script_path.replace('experiment', 'data')[:-3]

headers = ["pkid", "type", "basis_num"]
with open(f'{new_path}_test.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers once
    for prb in range(len(prbs)):
        for i in range(num_case):
            opt = CobylaOptimizer(max_iter=200)
            aer = DdsimProvider()
            solver = ChocoSolverSearch(
                prb_model=a[prb][i],  # 问题模型
                optimizer=opt,  # 优化器
                provider=aer,  # 提供器（backend + 配对 pass_mannager ）
                num_layers=10,
                shots=100000
            )
            result, depth = solver.search()
            writer.writerow([prb, 'basis_num', result])
            writer.writerow([prb, 'depth', depth])

