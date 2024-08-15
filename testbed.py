from Choco.model.lin_constr_bin_opt import LinearConstrainedBinaryOptimization as Model
if __name__ == '__main__':
    m = Model()
    num_1 = 1
    num_2 = 1
    m.addVar(name='jqf')

    x = m.addVars(num_1, name="x")
    y = m.addVars(num_2, num_1, name="y")
    m.setObjective(sum(3 * y[i, j] for i in range(num_2) for j in range(num_1)) + sum(4 * x[j] for j in range(num_1)), 'min')

    m.addConstrs((x[j] >= 1 for i in range(num_2) for j in range(num_1)))
    m.addConstrs([x[0] * x[0] == 1])
    obj = m.generate_obj_function()
    print(m)
    print(obj([1] * len(m.variables)))

    print(m.get_best_cost())
    # print(m.solve_with_gurobi())
    # m.optimize()