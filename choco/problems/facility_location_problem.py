from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from typing import Iterable

class FacilityLocationProblem(LcboModel):
    def __init__(self, num_demands: int, num_facilities: int, c: Iterable[Iterable],f: Iterable, fastsolve=True) -> None:
        super().__init__()
        self.num_demands = num_demands
        self.num_facilities = num_facilities
        self.c = c 
        self.f = f
         
        x = self.addVars(self.num_facilities, name="x")
        y = self.addVars(self.num_demands, self.num_facilities, name="y")
        self.setObjective(sum(self.c[i][j] * y[i, j] for i in range(self.num_demands) for j in range(self.num_facilities)) + sum(self.f[j] * x[j] for j in range(self.num_facilities)), 'min')
        self.addConstrs((sum(y[i, j] for j in range(self.num_facilities)) == 1 for i in range(self.num_demands)))
        self.addConstrs((y[i, j] <= x[j] for i in range(self.num_demands) for j in range(self.num_facilities)))

    def get_feasible_solution(self):
        """ 根据约束寻找到一个可行解
        """
        import numpy as np
        # for j in range(self.n):
        lst = np.zeros(len(self.variables))
        lst[0] = 1
        for i in range(self.num_demands):
            lst[self.num_facilities + self.num_facilities * i] = 1
        # for i in range(self.m):
        #     for j in range(self.n):
        #         self.Z[i][j].set_value(-self.Y[i][j].x + self.X[j].x)
        return lst

import random

def generate_flp(num_problems_per_scale, scale_list, min_value=1, max_value=20):
    def generate_random_flp(num_problems, idx_scale, m, n, min_value=1, max_value=20):
        problems = []
        configs = []
        for _ in range(num_problems):
            transport_costs = [[random.randint(min_value, max_value) for _ in range(n)] for _ in range(m)]
            facility_costs = [random.randint(min_value, max_value) for _ in range(n)]
            problem = FacilityLocationProblem(m, n, transport_costs, facility_costs)
            # if all(x in [-1, 0, 1]  for row in problem.driver_bitstr for x in row) : 
            problems.append(problem)
            configs.append((idx_scale, m, n, transport_costs, facility_costs))
        return problems, configs

    problem_list = []
    config_list = []
    for idx_scale, (m, n) in enumerate(scale_list):
        problems, configs = generate_random_flp(num_problems_per_scale, idx_scale, m, n, min_value, max_value)
        problem_list.append(problems)
        config_list.append(configs)
    
    return problem_list, config_list
