from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from typing import Iterable

class JobSchedulingProblem(LcboModel):
    def __init__(self, num_jobs: int, num_machines: int, c: Iterable[Iterable],Cap: Iterable, fastsolve=True) -> None:
        super().__init__()
        self.num_jobs = num_jobs
        self.num_machines = num_machines
        self.c = c 
        self.Cap = Cap
        x = self.addVars(self.num_jobs, self.num_machines, name="x")
        self.setObjective(sum(self.c[i][j] * x[i, j] for i in range(self.num_jobs) for j in range(self.num_machines)), 'min')
        self.addConstrs((sum(x[i, j] for j in range(self.num_machines)) == 1 for i in range(self.num_jobs)))
        self.addConstrs((sum(x[i, j] for i in range(self.num_jobs)) <= self.Cap[j] for j in range(self.num_machines)))

    def get_feasible_solution(self):
        """ 根据约束寻找到一个可行解
        """
        import numpy as np
        # for j in range(self.n):
        lst = np.zeros(len(self.variables))
        i=0
        for j in range(self.num_machines):
            for _ in range(self.Cap[j]):
                if i >= self.num_jobs:
                    break
                lst[i*self.num_machines + j] = 1
                i+=1
        anciIdx = 0
        for j in range(self.num_machines):
            anciSdx =0
            if sum(lst[i*self.num_machines + j] for i in range(self.num_jobs)) < self.Cap[j]:
                diff = (self.Cap[j]-sum(lst[i*self.num_machines + j] for i in range(self.num_jobs)))
                for _ in range((int)(self.Cap[j]-sum(lst[i*self.num_machines + j] for i in range(self.num_jobs)) )):
                    lst[self.num_machines*self.num_jobs+anciIdx+anciSdx]=1
                    anciSdx +=1
            anciIdx += self.Cap[j]
        return lst
        # return [ 0.0, 1.0, 1.0, 0.0, 1.0,  0.0,  0.0, 0.0,  0.0, 1.0]


import random

def generate_jsp(num_problems_per_scale: int, scale_list: list, min_value: float=1, max_value: float=20):
    """ generate a list of random FLP problems with different scales

    Args:
        num_problems_per_scale (int): the number of problems per scale
        scale_list (list):  a list of tuples (m, n) representing the scale of the problem
        min_value (float, optional): the minimum value of the transport cost. Defaults to 1.
        max_value (float, optional): the maximum value of the transport cost. Defaults to 20.
        
    Returns:
        problem_list (list): a list of FLP problems
        config_list (list): a list of tuples (scale_idx, m, n, transport_costs, facility_costs) representing the configuration of each problem
    """

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
