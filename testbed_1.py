from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from choco.solvers.optimizers.non_gradient import Cobyla
from choco.solvers.qiskit.choco import ChocoSolver
from choco.solvers.qiskit.provider.aer import AerProvider

m = LcboModel()
x = m.addVars(3, name='x')
m.setObjective(-x[0] -x[1] -x[2], 'min')
m.addConstr(x[0]- x[1] + x[2] == 1)
print(m)
opt = Cobyla(max_iter=200)
aer = AerProvider()
csolver = ChocoSolver(prb_model=m, optimizer=opt, num_layers=5, provider=aer,mcx_mode="linear")
result = csolver.solve()
# eval = csolver.evaluation()
print(result)
# print(eval)