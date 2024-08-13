from collections import defaultdict
from typing import Dict, Tuple, Union

coeff_type = float

def set_coeff_type(type):
    global coeff_type
    coeff_type = type

class Variable:
    def __init__(self, name, type='any') -> None:
        self.name = name
        self.type = type
        self.x = None

    def to_expression(self):
        """将 Variable 转为 Expression, 处理加减乘除"""
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
        return Constraint(self.to_expression() , '<=', other)
    
    def __ge__(self, other):
        return Constraint(self.to_expression() , '>=', other)
    
    def __repr__(self):
        return f"{self.name}"

class Expression:
    def __init__(self, terms: Dict[Tuple[Variable, ...], Union[int, float]] = None):
        self.terms = {tuple(sorted(term, key=lambda var: var.name)): coeff for term, coeff in (terms or {}).items()}

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
    def __init__(self, expr: Expression, sense, rhs: int):
        self.expr = expr
        self.sense = sense
        self.rhs = rhs

    def __repr__(self):
        return f"{self.expr} {self.sense} {self.rhs}"

class Model:
    def __init__(self):
        self.variables = []
        self.constraints = []
        self.objective = None
        self.obj_sense = None

    def addVar(self, vtype='C', name=""):
        var = Variable(name, vtype)
        self.variables.append(var)
        return var

    def setObjective(self, expression, sense):
        self.objective = expression
        self.obj_sense = sense

    def addConstr(self, constraint: Constraint):
        self.constraints.append(constraint)

    def optimize(self):
        # For simplicity, let's assume we solve the problem here and find optimal values.
        # In a real implementation, you would need a solver to handle this part.
        # Here we just assign some dummy values for the sake of demonstration.
        for var in self.variables:
            var.x = 0  # Set all variables to 0 as a dummy solution
        # Let's assume the optimal objective value is 0 for this dummy solution
        self.objVal = 0

    def __repr__(self):
        var_str = "   ".join([repr(var)+f" (type: {var.type})" for var in self.variables])
        constr_str = "\n".join([repr(constr) for constr in self.constraints])
        return (f"model:\n"
                f"variables:\n{var_str}\n\n"
                f"obj:\n{self.obj_sense} {self.objective}\n\n"
                f"s.t.:\n{constr_str}\n\n"
                )

if __name__ == '__main__':
    set_coeff_type(float)
    # Example of usage
    m = Model()

    # Create variables
    x = m.addVar(vtype='B', name="x")
    y = m.addVar(vtype='B', name="y")
    z = m.addVar(vtype='B', name="z")

    # Set objective function
    m.setObjective(x - y  + 2 * z, 'max')

    # Add constraints
    m.addConstr(x - 2 * y + 3 * z <= 4)
    m.addConstr(x - y >= 1)
    m.addConstr(x - y >= 1)
    m.addConstr(x >= 1)
    m.addConstr(x + 3*y == 1)

    # Solve it!
    m.optimize()
    print(m)
    print(f"optimal objective value: {m.objVal}")
    print(f"solution values: x={x.x}, y={y.x}, z={z.x}")

