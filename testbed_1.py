should_print = True

from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, ChocoSolverSearch, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

# model ----------------------------------------------
m = LcboModel()
x = m.addVars(5, name="x")
m.setObjective(x[0].to_expression(), "max")
m.addConstr(x[0] + x[1] == 1)
# exit()
m.addConstr(2 * x[3] >= 0)


m.set_penalty_lambda(0)
print(m)
optimize = m.optimize()
print(f"optimize_cost: {optimize}\n\n")
# sovler ----------------------------------------------
opt = CobylaOptimizer(max_iter=200)
aer = DdsimProvider()
solver = ChocoSolver(
    prb_model=m,  # 问题模型
    optimizer=opt,  # 优化器
    provider=aer,  # 提供器（backend + 配对 pass_mannager ）
    num_layers=1,
    # mcx_mode="linear",
)

result = solver.solve()
eval = solver.evaluation()
print(result)
print(eval)
