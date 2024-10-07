should_print = True

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, ChocoSolverMid, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 5
a, b = generate_flp(num_case,[(1, 2), (2, 3), (3, 3), (3, 4)], 1, 100)
# print(a[0][0])
# (1, [(2, 1), (3, 2), (3, 3), (4, 3), (4, 4)], 1, 20)

best_lst = []
arg_lst = []

import os
import csv
script_path = os.path.abspath(__file__)
new_path = script_path.replace('experiment', 'data')[:-3]

headers = ["pkid", "pid", "basis_num"]
with open(f'{new_path}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(headers)  # Write headers once
    for prb in range(4):
        for i in range(num_case):
            opt = CobylaOptimizer(max_iter=200)
            aer = DdsimProvider()
            solver = ChocoSolverMid(
                prb_model=a[prb][i],  # 问题模型
                optimizer=opt,  # 优化器
                provider=aer,  # 提供器（backend + 配对 pass_mannager ）
                num_layers=15,
                shots=100000
            )
            result = solver.search()
            writer.writerow([prb, i, result])

