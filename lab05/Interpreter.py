import copy
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from visit import *
import sys

sys.setrecursionlimit(10000)

class OperationManager:
    def __init__(self):
        self.operators = {
            '+': self.add,
            '-': self.sub,
            '*': self.mul,
            '/': self.div,
            '.+': self.dotadd,
            '.-': self.dotsub,
            '.*': self.dotmul,
            './': self.dotdiv,
            '==': self.eq,
            '!=': self.ne,
            '>': self.g,
            '<': self.l,
            '>=': self.ge,
            '<=': self.le
        }

    # Funkcja do wykonywania operacji
    def calculate(self, left_side, operator, right_side):
        return self.operators[operator](left_side, right_side)

    # Dodawanie
    def add(self, left_side, right_side):
        if isinstance(left_side, list):
            if len(left_side) > 0:
                if isinstance(left_side[0], list):  # sprawdzamy czy mamy do czynienia z macierza
                    # dodawanie w macierzy za pomoca funkcji lambda
                    return list(map(lambda l: list(map(lambda x: x[0]+x[1], list(zip(l[0], l[1])))), list(zip(left_side, right_side))))
                
                # dodawanie w liscie za pomoca funkcji lambda
                return list(map(lambda x: x[0]+x[1], list(zip(left_side, right_side))))
            return []
        return left_side + right_side

    # Odejmowanie
    def sub(self, left_side, right_side):
        if isinstance(left_side, list):
            if len(left_side) > 0:
                if isinstance(left_side[0], list):  # sprawdzanie czy mamy do czynienia z macierza
                    # odejmowanie w macierzy za pomoca funkcji lambda
                    return list(map(lambda l: list(map(lambda x: x[0] - x[1], list(zip(l[0], l[1])))), list(zip(left_side, right_side))))
                
                # odejmowanie w liscie za pomoca funkji lmabda
                return list(map(lambda x: x[0] - x[1], list(zip(left_side, right_side))))
            return []
        return left_side - right_side

    # Mnożenie
    def mul(self, left_side, right_side):
        if isinstance(left_side, list):
            resultMatrix = [[0 for x in range(len(left_side))] for y in range(len(right_side[0]))]
            for i in range(len(left_side)):
                for j in range(len(right_side[0])):
                    for k in range(len(right_side)):
                        resultMatrix[i][j] += left_side[i][k] * right_side[k][j]
            return resultMatrix
        else:
            return left_side * right_side

    # Dzielenie
    def div(self, left_side, right_side):
        return left_side / right_side


    # Funkcja do operacji na macierzach
    def dotop(self, op, a, b):
        if isinstance(a, list) and not isinstance(b, list):
            if len(a) > 0:
                if isinstance(a[0], list):
                    return list(map(lambda l: list(map(lambda x: op(x, b), l)), a))
                return list(map(lambda x: op(x, b), a))
            return []
        
        elif not isinstance(a, list) and isinstance(b, list):
            if len(b) > 0:
                if isinstance(b[0], list):
                    return list(map(lambda l: list(map(lambda x: op(x, a), l)), b))
                return list(map(lambda x: op(x, a), b))
            return []
        
        else:
            if len(a) == 0:
                return [[]]
            res1 = copy.deepcopy(a)
            
            if isinstance(a[0], list):
                for i in range(len(a)):
                    for j in range(len(a[i])):
                        res1[i][j] = op(a[i][j], b[i][j])
            else:
                for i in range(len(a)):
                    res1[i] = op(a[i], b[i])
            return res1

    def dotadd(self, a, b):
        return self.dotop(self.add, a, b)

    def dotsub(self, a, b):
        return self.dotop(self.sub, a, b)

    def dotmul(self, a, b):
        return self.dotop(self.mul, a, b)

    def dotdiv(self, a, b):
        return self.dotop(self.div, a, b)

    def eq(self, a, b):
        return a.__str__() == b.__str__()

    def ne(self, a, b):
        return a.__str__() != b.__str__()

    def g(self, left_side, right_side):
        return left_side > right_side

    def l(self, left_side, right_side):
        return left_side < right_side

    def ge(self, left_side, right_side):
        return left_side >= right_side

    def le(self, left_side, right_side):
        return left_side <= right_side


class Interpreter(object):
    def __init__(self):
        self.memory = MemoryStack()
        self.operationManager = OperationManager()

    @on('node')
    def visit(self, node):
        pass
    
    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Expression)
    def visit(self, node):
        left_side = node.left_side.accept(self)
        right_side = node.right_side.accept(self)
        operator = node.operator
        return self.operationManager.calculate(left_side, operator, right_side)

    @when(AST.Instructions)
    def visit(self, node):
        for instruction in node.children:
            instruction.accept(self)

    @when(AST.For)
    def visit(self, node):
        id = node.id
        ne1 = node.ne1.accept(self)
        ne2 = node.ne2.accept(self)

        self.memory.push(None)
        self.memory.insert(id, ne1)
        while self.memory.get(id) < ne2:
            try:
                self.memory.push(None)
                node.instruction.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memory.set(id, self.memory.get(id) + 1)
                self.memory.pop()
        self.memory.pop()

    @when(AST.While)
    def visit(self, node):
        while node.expression.accept(self):
            try:
                self.memory.push(None)
                node.instruction.accept(self)
            except ContinueException:
                continue
            except BreakException:
                break
            finally:
                self.memory.pop()

    @when(AST.Block)
    def visit(self, node):
        self.memory.push(None)
        node.body.accept(self)
        self.memory.pop()

    @when(AST.Assignment)
    def visit(self, node):

        if isinstance(node.left_side, AST.Range):
            current_val = self.memory.get(node.left_side.var.name)
            x = node.left_side.fun_body[0].accept(self)
            y = node.left_side.fun_body[1].accept(self)
            if node.assignment == '=':
                current_val[x][y] = node.value.accept(self)
            else:
                current_val[x][y] = self.operationManager.calculate(current_val[x][y], node.assignment[0], node.value.accept(self))
            self.memory.set(node.left_side.var.name, current_val)
            
        else:
            if node.assignment == '=':
                self.memory.set(node.left_side.name, node.value.accept(self))
            else:
                current_val = self.memory.get(node.left_side.name)
                self.memory.set(node.left_side.name,
                                self.operationManager.calculate(current_val, node.assignment[0], node.value.accept(self)))

    @when(AST.Range)
    def visit(self, node):
        current_val = self.memory.get(node.var.name)
        x = node.fun_body[0].accept(self)
        y = node.fun_body[1].accept(self)
        return current_val[x][y]

    @when(AST.Integer)
    def visit(self, node):
        return node.value

    @when(AST.Float)
    def visit(self, node):
        return node.value

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.Vector)
    def visit(self, node):
        body = []
        for coordinate in node.body:
            body.append(coordinate.accept(self))
        return body

    @when(AST.Matrix)
    def visit(self, node):
        body = []
        for row in node.body:
            body.append(row.accept(self))
        return body

    @when(AST.Function)
    def visit(self, node):

        args = []
        for arg in node.fun_body:
            args.append(arg.accept(self))

        value = None

        if node.fun_name == 'eye':
            return [[1 if c == r else 0 for c in range(args[0])] for r in range(args[0])]
        elif node.fun_name == 'zeros':
            value = 0
        elif node.fun_name == 'ones':
            value = 1

        if len(args) < 2:
            args.append(args[0])

        return [[ value for c in range(args[1])] for r in range(args[0])]


    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(node.instruction.accept(self))


    @when(AST.Print)
    def visit(self, node):
        visitedValues  = []
        for arg in node.body:
            visitedValues.append(arg.accept(self))
        print(*visitedValues, sep=', ')

    @when(AST.Id)
    def visit(self, node):
        return self.memory.get(node.name)

    @when(AST.If)
    def visit(self, node):
        expression = node.expression.accept(self)
        if expression:
            self.memory.push(None)
            node.instruction1.accept(self)
            self.memory.pop()
        elif node.instruction2 is not None:
            self.memory.push(None)
            node.instruction2.accept(self)
            self.memory.pop()


