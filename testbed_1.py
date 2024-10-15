should_print = True

from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers import CobylaOptimizer, AdamOptimizer
from choco.solvers.qiskit import (
    ChocoSolver, ChocoSolverSearch, CyclicSolver, HeaSolver, PenaltySolver, NewSolver, NewXSolver,
    AerGpuProvider, AerProvider, FakeBrisbaneProvider, FakeKyivProvider, FakeTorinoProvider, DdsimProvider,
)

# model ----------------------------------------------
m = LcboModel()
x = m.addVars(6, name="x")
m.setObjective(x[0] + x[1] + x[2], "max")
# m.addConstr(x[0] + x[1] + x[2] == 2)
# m.addConstr(x[0] + x[1] == 1)
# exit()
m.addConstr(x[0] + x[1] == 1)
m.addConstr(x[2] + x[3] == 1)
m.addConstr(x[4] + x[5] == 1)
m.addConstr(x[0] + x[2]   == 1)


print(m.lin_constr_mtx)
# exit()
# m.set_penalty_lambda(0)
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
    num_layers=7,
    # mcx_mode="linear",
)
print(solver.circuit_analyze(['depth', 'width', 'culled_depth', 'num_one_qubit_gates']))
# print(solver.search())
# result = solver.solve()
# eval = solver.evaluation()
# print(result)
# print(eval)
