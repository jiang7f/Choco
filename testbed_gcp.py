should_print = True

from choco.problems.graph_coloring_problem import GraphColoringProblem, generate_gcp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 100
a = GraphColoringProblem(num_case, [(3, 1), (3, 2), (4, 2), (4, 3)])
best_lst = []
arg_lst = []
for i in range(num_case):
    opt = CobylaOptimizer(max_iter=200)
    aer = DdsimProvider()
    solver = NewSolver(
        prb_model=a,  # 问题模型
        optimizer=opt,  # 优化器
        provider=aer,  # 提供器（backend + 配对 pass_mannager ）
        num_layers=7,
        shots=1024
        # mcx_mode="linear",
    )

    result = solver.solve()
    u, v, w, x = solver.evaluation()
    print(f"{i}: {u}, {v}, {w}, {x}")
    best_lst.append(u)
    arg_lst.append(w)

print(sum(best_lst) / num_case, sum(arg_lst) / num_case)
