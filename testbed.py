from Choco.model.lin_constr_bin_opt import LinearConstrainedBinaryOptimization as Model
if __name__ == '__main__':
    m = Model()
    num_facilities = 1
    num_demands = 1
    m.addVar(name='jqf')
    x = m.addVars(num_facilities, name="x")
    y = m.addVars(num_demands, num_facilities, name="y")
    m.setObjective(sum(3 * y[i, j] for i in range(num_demands) for j in range(num_facilities)) + sum(4 * x[j] for j in range(num_facilities)), 'min')

    m.addConstrs((x[j] >= 1 for i in range(num_demands) for j in range(num_facilities)))
    obj = m.generate_obj_function()
    print(m)
    print(obj([1] * len(m.variables)))

    print(m.get_best_cost())
    # print(m.solve_with_gurobi())
    # m.optimize()