should_print = True

from choco.problems.facility_location_problem import generate_flp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver, ChocoSolverSearch,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)
from choco.solvers.technology.eliminate import Eliminate_variables

num_case = 1
a, b = generate_flp(num_case,[(1, 2)], 1, 100)
# print(a[0][0])
# (1, [(2, 1), (3, 2), (3, 3), (4, 3), (4, 4)], 1, 20)

best_lst = []
arg_lst = []

result_lst = []

for i in range(num_case):
    opt = CobylaOptimizer(max_iter=200)
    aer = DdsimProvider()
    e_solver = Eliminate_variables(
        solver=ChocoSolver,
        prb_model=a[0][i],  # 问题模型
        optimizer=opt,  # 优化器
        provider=aer,  # 提供器（backend + 配对 pass_mannager ）
        num_layers=3,
        shots=1024,
        # mcx_mode="linear",
        num_frozen_qubit=1,
    )

    result = e_solver.solve()
    print(e_solver.depth())
    result_lst.append(result)

print(result_lst)
