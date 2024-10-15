should_print = True

from choco.problems.cnst_demo import ConstraintsDemo
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 200
# print(a[0][0])
# (1, [(2, 1), (3, 2), (3, 3), (4, 3), (4, 4)], 1, 20)

result_best_lst = []
result_arg_lst = []
result_incnst_lst = []
result_iter_lst = []
num_qubit = 12
num_cnst = num_qubit // 2
for i in range(num_cnst):
    best_lst = []
    arg_lst = []
    incnst_lst = []
    iter_lst = []
    for j in range(num_case):
        a = ConstraintsDemo(num_qubit, i)
        opt = CobylaOptimizer(max_iter=1000)
        aer = DdsimProvider()
        solver = ChocoSolver(
            prb_model=a,  # 问题模型
            optimizer=opt,  # 优化器
            provider=aer,  # 提供器（backend + 配对 pass_mannager ）
            num_layers=4,
            shots=1024
            # mcx_mode="linear",
        )

        result = solver.solve()
        u, v, w, x = solver.evaluation()
        print(f"{i}: {u}, {v}, {w}, {x}")
        best_lst.append(u)
        incnst_lst.append(v)
        arg_lst.append(w)
        iter_lst.append(x)

    result_best_lst.append(sum(best_lst) / num_case)
    result_arg_lst.append(sum(arg_lst) / num_case)
    result_incnst_lst.append(sum(incnst_lst) / num_case)
    result_iter_lst.append(sum(iter_lst) / num_case)

print()
print(">>>>>>>>>>>>>>")
print()
for a, b, c, d in zip(result_best_lst, result_incnst_lst, result_arg_lst, result_iter_lst):
    print(a, b, c, d)

