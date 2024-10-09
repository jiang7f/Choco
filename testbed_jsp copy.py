should_print = True

from choco.problems.job_scheduling_problem import JobSchedulingProblem, generate_jsp
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 5
a, b = generate_jsp(num_case, [(2, 2), (3, 3)], 1, 20)


for prbs in range(len(a)):
    best_lst = []
    in_cnst_list = []
    arg_lst = []
    iter_lst = []
    for i in range(num_case):
        opt = CobylaOptimizer(max_iter=200)
        aer = DdsimProvider()
        solver = ChocoSolver(
            prb_model=a[prbs][i],  # 问题模型
            optimizer=opt,  # 优化器
            provider=aer,  # 提供器（backend + 配对 pass_mannager ）
            num_layers=10,
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

    print(">>>>>>>>", sum(best_lst) / num_case, sum(in_cnst_list) / num_case, sum(arg_lst) / num_case, sum(iter_lst) / num_case)

