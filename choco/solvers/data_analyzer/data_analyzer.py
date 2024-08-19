from ...utils import iprint
from typing import List
import numpy as np

class DataAnalyzer():
    def __init__(self, best_cost, collapse_state_lst: List, probs_lst: List, obj_dir, obj_func, lin_constr_mtx):
        self.best_cost = best_cost
        self.states_probs_zip = zip(collapse_state_lst, probs_lst)
        self.obj_dir = obj_dir
        self.obj_func = obj_func
        self.lin_constr_mtx = lin_constr_mtx
    
    def summary(self):
        best_cost = self.best_cost

        data_metrics_lst = []
        for collapse_state, probs in self.states_probs_zip:
            mean_cost = 0
            best_solution_probs = 0
            in_constraints_probs = 0
            for cs, pr in zip(collapse_state, probs):
                pcost = self.obj_dir * self.obj_func(cs)
                if pr >= 1e-3:
                    iprint(f'{cs}: {pcost} - {pr}')
                if all([np.dot(cs,constr[:-1]) == constr[-1] for constr in self.lin_constr_mtx]):
                    in_constraints_probs += pr
                    if pcost == best_cost:
                        best_solution_probs += pr
                mean_cost += pcost * pr
            best_solution_probs *= 100
            in_constraints_probs *= 100
            # maxprobidex = np.argmax(probs)
            # max_prob_solution = collapse_state[maxprobidex]
            # cost = self.obj_dir * self.obj_func(max_prob_solution)
            ARG = abs((mean_cost - best_cost) / best_cost)
            # iprint(f"max_prob_solution: {max_prob_solution}, cost: {cost}, max_prob: {probs[maxprobidex]:.2%}") #-
            iprint(f'best_solution_probs: {best_solution_probs}')
            iprint(f'in_constraint_probs: {in_constraints_probs}')
            iprint(f'ARG: {ARG}')
            iprint(f"mean_cost: {mean_cost}")
            data_metrics_lst.append([best_solution_probs, in_constraints_probs, ARG])
        
        return data_metrics_lst