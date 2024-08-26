should_print = True

from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, CyclicSolver, HeaSolver, PenaltySolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

# model ----------------------------------------------
m = LcboModel()
x = m.addVars(4, name="x")
m.setObjective(x[0] + x[1] + x[2] + x[3], "max")
m.addConstr(x[0] + x[1] + x[2] == 1)
m.addConstr(x[1] + x[2] + x[3] == 1)
# m.set_penalty_lambda(0)
print(m)
optimize = m.optimize()
print(f"optimize_cost: {optimize}\n\n")
# sovler ----------------------------------------------
opt = CobylaOptimizer(max_iter=200)
aer = DdsimProvider()
solver = HeaSolver(
    prb_model=m,  # 问题模型
    optimizer=opt,  # 优化器
    provider=aer,  # 提供器（backend + 配对 pass_mannager ）
    num_layers=5,
    # mcx_mode="linear",
)

result = solver.solve()
eval = solver.evaluation()
print(result)
print(eval)
