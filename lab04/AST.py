class Node(object):
    pass


class Function(Node):
    def __init__(self, fun_name, fun_body, line_number=None):
        self.line_number = line_number
        self.fun_name = fun_name
        self.fun_body = fun_body


class Block(Node):
    def __init__(self, body, line_number=None):
        self.line_number = line_number
        self.body = body

class Instructions(Node):

    def __init__(self, instruction, line_number=None):

        self.line_number = line_number
        self.children = [instruction]


class FlowKeyword(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number
        self.value = value


class For(Node):
    def __init__(self, id, ne1, ne2, instruction, line_number=None):
        self.line_number = line_number
        self.id = id
        self.ne1 = ne1
        self.ne2 = ne2
        self.instruction = instruction


class While(Node):
    def __init__(self, expression, instruction, line_number=None):
        self.line_number = line_number

        self.expression = expression
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, left_side, assignment, value, line_number=None):
        self.line_number = line_number

        self.left_side = left_side
        self.assignment = assignment
        self.value = value


class Expression(Node):
    def __init__(self, left_side, operator, right_side, line_number=None):
        self.line_number = line_number

        self.left_side = left_side
        self.operator = operator
        self.right_side = right_side


class Transposition(Node):
    def __init__(self, factor, line_number=None):
        self.line_number = line_number
        self.factor = factor


class UMinus(Node):
    def __init__(self, factor, line_number=None):
        self.line_number = line_number
        self.factor = factor


class Print(Node):
    def __init__(self, body, line_number=None):
        self.line_number = line_number
        self.body = body


class String(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value


class Integer(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value


class Id(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.name = value


class Float(Node):
    def __init__(self, value, line_number=None):
        self.line_number = line_number

        self.value = value


class Matrix(Node):
    def __init__(self, body=None, line_number=None):
        self.line_number = line_number
        self.body = body

class Range(Node):
    def __init__(self, var, fun_body, line_number=None):
        self.line_number = line_number

        self.var = var
        self.fun_body = fun_body


class Vector(Node):
    def __init__(self, body=[], line_number=None):
        self.line_number = line_number
        self.body = body


class If(Node):
    def __init__(self, expression, instruction1, instruction2=None, line_number=None):
        self.line_number = line_number

        self.expression = expression
        self.instruction1 = instruction1
        self.instruction2 = instruction2


class Return(Node):
    def __init__(self, instruction=None, line_number=None):
        self.line_number = line_number
        self.instruction = instruction

class Error(Node):
    def __init__(self):
        pass
