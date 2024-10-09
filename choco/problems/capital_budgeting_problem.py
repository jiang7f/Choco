from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from typing import Iterable

class CapitalBudgetingProblem(LcboModel):
    def __init__(self, input: Iterable[int], revenue: Iterable[int], budget: int, dependence:Iterable[tuple]) -> None:
        super().__init__()
        # 投资项目总数
        self.num_project = len(input)
        self.input = input
        self.revenue = revenue
        self.budget = budget
        self.dependence = dependence
         
        x = self.addVars(self.num_project, name="x")
        self.setObjective(sum(self.revenue[i] * x[i] for i in range(self.num_project)), 'max')
        self.addConstr((sum(input[i] * x[i] for i in range(self.num_project))) <= self.budget)
        self.addConstrs((x[i] <= x[j] for i, j in self.dependence))

    def get_feasible_solution(self):
        """ 根据约束寻找到一个可行解
        """
        import numpy as np
        lst = np.zeros(len(self.variables))
        for i in range(self.num_project, self.num_project + self.budget):
            lst[i] = 1
        return lst

import random

def generate_flp(num_problems_per_scale, scale_list, min_value=1, max_value=20):
    def generate_random_flp(num_problems, idx_scale, m, n, min_value=1, max_value=20):
        problems = []
        configs = []
        for _ in range(num_problems):
            transport_costs = [[random.randint(min_value, max_value) for _ in range(n)] for _ in range(m)]
            facility_costs = [random.randint(min_value, max_value) for _ in range(n)]
            problem = CapitalBudgetingProblem(m, n, transport_costs, facility_costs)
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
