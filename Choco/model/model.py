from collections import defaultdict
from typing import Dict, Tuple, Union, List, Set
from itertools import product

coeff_type = int
to_lin_constr: bool = True

def set_coeff_type(type_):
    global coeff_type
    coeff_type = type_

def set_to_lin_constr(flag: bool):
    # 暂时默认只有线性约束       
    global to_lin_constr
    to_lin_constr = flag

class Variable:
    def __init__(self, vtype='binary', name="unnamed"):
        self.vtype = vtype
        self.name = name
        self.x = None

    def to_expression(self):
        """将 Variable 转为 Expression, 处理加减乘除/生成约束"""
        return Expression({tuple([self]): coeff_type(1)})

    def __neg__(self):
        return -1 * self.to_expression()

    def __add__(self, other):
        return self.to_expression() + other

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self.to_expression() - other

    def __mul__(self, other):
        return self.to_expression() * other

    def __rmul__(self, other):
        return self * other

    # def __truediv__(self, other):
    #     return self.to_expression() / other
    def __le__(self, other):
        return Constraint(self.to_expression(), '<=', other)
    
    def __ge__(self, other):
        return Constraint(self.to_expression(), '>=', other)

    def __eq__(self, other):
        return Constraint(self.to_expression(), '==', other)

    def __hash__(self):
        return hash(self.name)

    def __repr__(self):
        return f"{self.name}"

class Expression:
    def __init__(self, terms: Dict[Tuple[Variable, ...], Union[int, float]] = None):
        self.terms = {tuple(sorted(term, key=lambda var: var.name)): coeff for term, coeff in (terms or {}).items()}
    
    def extract_constants(self):
        """提取常数项，并从表达式中移除"""
        if () in self.terms:
            constant = self.terms.pop(())
            return constant
        return coeff_type(0)
    
    def __add__(self, other):
        result = defaultdict(coeff_type, self.terms)
        if isinstance(other, (int, float)):
            other = Expression({(): coeff_type(other)})
        elif isinstance(other, Variable):
            other = other.to_expression()
        for var, coeff in other.terms.items():
            result[var] += coeff
        return Expression(result)
    
    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        return self + (-1 * other)

    def __rsub__(self, other):
        return -1 * self + other

    def __mul__(self, other):
        result = defaultdict(coeff_type)
        if isinstance(other, (int, float)):
            other = Expression({(): coeff_type(other)})
        elif isinstance(other, Variable):
            other = other.to_expression()
        for var_1, coeff_1 in self.terms.items():
            for var_2, coeff_2 in other.terms.items():
                combined_var = tuple(sorted(var_1 + var_2, key=lambda v: v.name))
                result[combined_var] += coeff_1 * coeff_2
        return Expression(result)

    def __rmul__(self, other):
        return self * other
    
    def __neg__(self):
        return -1 * self

    def __le__(self, other):
        return Constraint(self, '<=', other)
    
    def __ge__(self, other):
        return Constraint(self, '>=', other)
    
    def __eq__(self, other):
        return Constraint(self, '==', other)

    def __repr__(self):
        terms_repr = " + ".join(
            f"{coeff} * {' * '.join(str(var) for var in term)}" 
            for term, coeff in self.terms.items() 
            if term  # 特判，跳过键为空的情况
        )
        # 如果有常数项（空元组），并且系数不为0，添加到结果中
        if () in self.terms and self.terms[()] != 0:
            if terms_repr:
                terms_repr = f"{terms_repr} + {self.terms[()]}"
            else:
                terms_repr = f"{self.terms[()]}"
        return terms_repr

class Constraint:
    def __init__(self, expr: Expression, sense, rhs):
        if isinstance(rhs, Variable):
            rhs = rhs.to_expression()
        # 提取 rhs 中的常数项
        if isinstance(rhs, Expression):
            rhs_const = rhs.extract_constants()
            rhs_expr = rhs
        else:
            rhs_const = rhs
            rhs_expr = Expression()

        # 将 rhs 的非常数部分移到左边的表达式中
        self.expr = expr - rhs_expr
        self.sense = sense
        self.rhs = rhs_const

    def __repr__(self):
        return f"{self.expr} {self.sense} {self.rhs}"

class Model:
    def __init__(self):
        self.variables = []
        self.existing_var_names: Set[str] = set()
        self.constraints = []
        self.objective = None   
        self.obj_sense = None

    def addVar(self, vtype='binary', *, name):
        if name in self.existing_var_names:
            print(f"Variable with name '{name}' already exists.")
            return None
        
        self.existing_var_names.add(name)
        var = Variable(vtype, name)
        self.variables.append(var)
        return var
    
    def addVars(self, *dimensions, vtype='binary', name) -> Dict[Tuple[int, ...], Variable]:
        if name in self.existing_var_names:
            print(f"Variable with name '{name}' already exists.")
            return None

        self.existing_var_names.add(name)
        vars = {}
        # 为了同步gurobi的索引方式，要特殊处理一维情况
        is_single_dim = len(dimensions) == 1
        # 生成所有可能的索引组合
        dimension_ranges = [range(d) for d in dimensions]
        for index_tuple in product(*dimension_ranges):
            var_name = f"{name}_{'_'.join(map(str, index_tuple))}"
            var = Variable(vtype, var_name)
            self.variables.append(var)
            if is_single_dim:
                vars[index_tuple[0]] = var
            else:
                vars[index_tuple] = var
        return vars
    
    def setObjective(self, expression, sense):
        self.objective = expression
        self.obj_sense = sense

    def addConstr(self, constraint: Constraint):
        # if constraint.sense == '<=':
        #     self.addVar()
        #     constraint.expr =
        # elif constraint.sense == '>=':
        #     pass
        self.constraints.append(constraint)

    def addConstrs(self, constraints: List[Constraint]):
        for constr in constraints:
            self.addConstr(constr)

    def optimize(self):
        # Here we just assign some dummy values for the sake of demonstration.
        for var in self.variables:
            var.x = 0x7f
        # Let's assume the optimal objective value is 0 for this dummy solution
        self.objVal = 0xdb

    def __repr__(self):
        var_str = "   ".join([repr(var)+f" (type: {var.vtype})" for var in self.variables])
        constr_str = "\n".join([repr(constr) for constr in self.constraints])
        return (f"m:\n"
                f"variables:\n{var_str}\n\n"
                f"obj:\n{self.obj_sense} {self.objective}\n\n"
                f"s.t.:\n{constr_str}\n\n"
                )

if __name__ == '__main__':
    set_coeff_type(float)
    # Example of usage
    m = Model()

    # # Create variables
    # x = m.addVar(vtype='B', name="x")
    # y = m.addVar(vtype='B', name="y")
    # z = m.addVar(vtype='B', name="z")
    # hh = m.addVars(2,2, name='hh')
    # m.addConstr(sum(hh.values()))
    # # Set objective function
    # m.setObjective(x - y  + 2 * z, 'max')
    # m.addConstrs((hh[i,j] == 1 for i in range(1, 3) for j in range(1, 3)))
    # # Add constraints
    # m.addConstr(x - 2 * y + 3 * z <= 4)
    # m.addConstr(x - y >= 1)
    # m.addConstr(x - y >= 1)
    # m.addConstr(x >= 1)
    # m.addConstr(x + 3*y == 1)
    num_facilities = 3
    num_demands = 4
    x = m.addVars(num_facilities, vtype='binary', name="x")
    y = m.addVars(num_demands, num_facilities, vtype='binary', name="y")

    # Objective function
    m.setObjective(sum(3 * y[i, j] for i in range(num_demands) for j in range(num_facilities)) + sum(4 * x[j] for j in range(num_facilities)), 'min')

    # Constraints
    m.addConstrs((sum(y[i, j] for j in range(num_facilities)) == 1 for i in range(num_demands)))
    m.addConstrs((y[i, j] == x[j] for i in range(num_demands) for j in range(num_facilities)))
    # Solve it!
    # m.optimize()
    print(m)
    # print(f"optimal objective value: {m.objVal}")
    # print(f"solution values: x={x.x}, y={y.x}, z={z.x}")

