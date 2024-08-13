class Variable:
    def __init__(self, name, vtype):
        self.name = name
        self.vtype = vtype
        self.X = None
    
    def __add__(self, other):
        if isinstance(other, Variable):
            return Expression([self, other], [1, 1])
        else:
            return Expression([self], [1], other)
    
    def __radd__(self, other):
        return self + other
    
    def __mul__(self, other):
        return Expression([self], [other])
    
    def __rmul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-1 * other)
    
    def __rsub__(self, other):
        return other + (-1 * self)

    def __neg__(self):
        return -1 * self

    def __repr__(self):
        return f"{self.name}"

class Expression:
    def __init__(self, vars, coeffs, const=0):
        self.vars = vars
        self.coeffs = coeffs
        self.const = const
    
    def __add__(self, other):
        if isinstance(other, Variable):
            return Expression(self.vars + [other], self.coeffs + [1], self.const)
        elif isinstance(other, Expression):
            return Expression(self.vars + other.vars, self.coeffs + other.coeffs, self.const + other.const)
        else:
            return Expression(self.vars, self.coeffs, self.const + other)
    
    def __radd__(self, other):
        return self + other
    
    def __mul__(self, other):
        new_coeffs = [coeff * other for coeff in self.coeffs]
        return Expression(self.vars, new_coeffs, self.const * other)
    
    def __rmul__(self, other):
        return self * other
    
    def __sub__(self, other):
        return self + (-1 * other)
    
    def __rsub__(self, other):
        return -1 * self + other
    
    def __neg__(self):
        return -1 * self
    
    def __le__(self, other):
        return Constraint(self, '<=', other)
    
    def __ge__(self, other):
        return Constraint(self, '>=', other)
    
    def __eq__(self, other):
        return Constraint(self, '==', other)
    def __repr__(self):
        terms = [f"{coeff}{var}" if coeff != 1 else str(var) for var, coeff in zip(self.vars, self.coeffs)]
        if self.const:
            terms.append(str(self.const))
        return " + ".join(terms)
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

    def addConstr(self, constraint):
        self.constraints.append(constraint)

    def optimize(self):
        # For simplicity, let's assume we solve the problem here and find optimal values.
        # In a real implementation, you would need a solver to handle this part.
        # Here we just assign some dummy values for the sake of demonstration.
        for var in self.variables:
            var.X = 0  # Set all variables to 0 as a dummy solution
        # Let's assume the optimal objective value is 0 for this dummy solution
        self.objVal = 0

    def __repr__(self):
        var_str = "   ".join([repr(var)+f" (type: {var.vtype})" for var in self.variables])
        constr_str = "\n   ".join([repr(constr) for constr in self.constraints])
        return (f"Model:\n"
                f"{self.obj_sense} {self.objective}\n\n"
                f"s.t. :\n{constr_str}\n\n"
                f"Variables:\n{var_str}\n\n"
                )
# Example of usage
m = Model()

# Create variables
x = m.addVar(vtype='B', name="x")
y = m.addVar(vtype='B', name="y")
z = m.addVar(vtype='B', name="z")

# Set objective function
m.setObjective(x - y  + 2 * z, 'MAXIMIZE')

# Add constraints
m.addConstr(x - 2 * y + 3 * z <= 4)
m.addConstr(x - y >= 1)

# Solve it!
m.optimize()
print(m)
print(f"Optimal objective value: {m.objVal}")
print(f"Solution values: x={x.X}, y={y.X}, z={z.X}")
