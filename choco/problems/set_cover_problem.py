from choco.model import LinearConstrainedBinaryOptimization as LcboModel
from typing import Iterable, List, Tuple
class SetCoverProblem(LcboModel):
    def __init__(self, num_sets: int, list_element_belongs: List[List]) -> None:
        super().__init__()
        self.num_sets = num_sets
        self.list_element_belongs = list_element_belongs
        self.num_elements = len(self.list_element_belongs)

        self.x = x = self.addVars(num_sets, name='x')
        self.setObjective(sum(x[i] for i in range(num_sets)), 'min')
        self.addConstrs(sum(x[j] for j in belongs) >= 1 for belongs in list_element_belongs)

    def get_feasible_solution(self):
        """ 根据约束寻找到一个可行解 """
        import numpy as np
        fsb_lst = np.zeros(len(self.variables))
        for i in range(self.num_sets):
            fsb_lst[i] = 1
        self.fill_feasible_solution(fsb_lst)
        return fsb_lst
    

# ////////////////////////////////////////////////////

import random

def generate_scp(num_problems_per_scale, scale_list, min_value=1, max_value=20) -> Tuple[List[List[SetCoverProblem]], List[List[Tuple]]]:
    def split_into_parts(all_sets, num_parts, min_value, upper_limit):
        # 确保每个部分至少有 min_value 的长度
        parts = [min_value] * num_parts
        remaining = all_sets - min_value * num_parts
        
        # 随机分配剩余的长度，确保每个部分不超过 upper_limit
        while remaining > 0:
            # 随机选择一个部分，但只分配给长度小于 upper_limit 的部分
            idx = random.randint(0, num_parts - 1)
            if parts[idx] < upper_limit - 1:
                parts[idx] += 1
                remaining -= 1
        
        return parts
    
    def generate_random_scp(num_problems, idx_scale, num_sets, all_sets, min_value=1, max_value=20):
        upper_limit = min(max_value, num_sets)
        problems = []
        configs = []
        for _ in range(num_problems):
            list_element_belongs = []
            lengths = split_into_parts(all_sets, num_sets, min_value, upper_limit)
            for list_length in lengths:
                # 生成 [min_value, upper_limit) 范围内不重复的随机数列表
                random_list = random.sample(range(min_value, upper_limit), list_length)
                list_element_belongs.append(random_list)
            problem = SetCoverProblem(num_sets, list_element_belongs)
            if all(x in [-1, 0, 1]  for row in problem.driver_bitstr for x in row) : 
                problems.append(problem)
                configs.append((idx_scale, len(problem.variables), len(problem.lin_constr_mtx), num_sets, list_element_belongs))
        return problems, configs

    problem_list = []
    config_list = []
    for idx_scale, (num_sets, all_sets) in enumerate(scale_list):
        problems, configs = generate_random_scp(num_problems_per_scale, idx_scale, num_sets, all_sets, min_value, max_value)
        problem_list.append(problems)
        config_list.append(configs)
    
    return problem_list, config_list