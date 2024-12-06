# Implemetnacja abstrakcyjnego drzewa skladni

class Node(object):
    pass

# wyrażenia binarne
class BinExpr(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right


# wyrażenia relacyjne
class Condition(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right
          
class Number(Node):
    def __init__(self, value):
        self.value = value

class String(Node):
    def __init__(self, value):
        self.value = value

class Variable(Node):
    def __init__(self, name):
        self.name = name
    

# instrukcje warunkowe if-else
class If(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction

class IfElse(Node):
    def __init__(self, condition, if_instruction, else_instruction):
        self.condition = condition
        self.if_instruction = if_instruction
        self.else_instruction = else_instruction
        
        
# pętle: while oraz for
class While(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction
        
class For(Node):
    def __init__(self, var, range, instruction):
        self.var = var
        self.range = range
        self.instruction = instruction

class Range(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end


# instrukcje break, continue oraz return     
class Break(Node):
    def __init__(self):
        pass

class Continue(Node):
    def __init__(self):
        pass
    
class Return(Node):
    def __init__(self, value):
        self.value = value
        
        
# instrukcje print
class Print(Node):
    def __init__(self, values):
        self.values = values

class PrintValues(Node):
    def __init__(self, value, values=None):
        self.values = values.values.copy() if values else []
        self.values.append(value)
        
        
# instrukcje zlozone
class Instructions(Node):
    def __init__(self, instruction, instructions=None):
        self.instructions = instructions.instructions if instructions else []
        self.instructions.append(instruction)
        
class Assignment(Node):
    def __init__(self, variable, operator, expression):
        self.variable = variable
        self.operator = operator
        self.expression = expression

class Uminus(Node):
    def __init__(self, expression):
        self.expression = expression
        
class Transposition(Node):
    def __init__(self, matrix):
        self.matrix = matrix
        
        
# tablice
class Matrix(Node):
    def __init__(self, vector, old_matrix=None):
        self.matrix = old_matrix.matrix.copy() if old_matrix else []
        self.matrix.append(vector)
        
class MatrixElement(Node):
    def __init__(self, id, row_idx, col_idx):
        self.id = id
        self.row_idx = row_idx
        self.col_idx = col_idx
        
class MatrixFunction(Node):
    def __init__(self, function_name, function_arg):
        self.function_name = function_name
        self.function_arg = function_arg

class Vector(Node):
    def __init__(self, elem, old_vector=None):
        self.vector = old_vector.vector.copy() if old_vector else []
        self.vector.append(elem)
        
class VectorElement(Node):
    def __init__(self, id, index):
        self.id = id
        self.index = index
        
class Error(Node):
    def __init__(self):
        pass
      