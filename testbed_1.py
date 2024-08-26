should_print = True

from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

# model ----------------------------------------------
m = LcboModel()
x = m.addVars(3, name="x")
m.setObjective(x[0] + x[1] + x[2], "min")
m.addConstr(x[0] - x[1] + x[2] == 1)
# m.set_penalty_lambda(0)
print(m)
optimize = m.optimize()
print(f"optimize_cost: {optimize}\n\n")
# sovler ----------------------------------------------
opt = AdamOptimizer(max_iter=200)
aer = DdsimProvider()
choco_solver = ChocoSolver(
    prb_model=m,  # 问题模型
    optimizer=opt,  # 优化器
    provider=aer,  # 提供器（backend + 配对 pass_mannager ）
    num_layers=5,
    mcx_mode="linear",
)
result = choco_solver.solve()
eval = choco_solver.evaluation()
print(result)
print(eval)
