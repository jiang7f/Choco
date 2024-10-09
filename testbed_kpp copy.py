should_print = True

from choco.problems.k_partition_problem import KPartitionProblem, generate_kpp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 1
a, b = generate_kpp(num_case, [(4, 2, 3), (6, 3, 5), (8, 3, 7), (9, 3, 8)], 1, 20)
best_lst = []
best_lst = []
arg_lst = []
for i in range(num_case):
    opt = CobylaOptimizer(max_iter=200)
    aer = DdsimProvider()
    solver = ChocoSolver(
        prb_model=a[0][i],  # 问题模型
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
    arg_lst.append(w)

print(sum(best_lst) / num_case, sum(arg_lst) / num_case)
