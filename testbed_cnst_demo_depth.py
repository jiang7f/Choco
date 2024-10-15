should_print = True

from choco.problems.cnst_demo import ConstraintsDemo
from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

num_case = 1
# print(a[0][0])
# (1, [(2, 1), (3, 2), (3, 3), (4, 3), (4, 4)], 1, 20)

result_best_lst = []
result_arg_lst = []
result_incnst_lst = []
result_iter_lst = []
num_qubit = 6
num_cnst = num_qubit // 2

lst = []
for i in range(num_cnst):
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
        depth = solver.circuit.inference_circuit.depth()
        lst.append(depth)
    print(lst)