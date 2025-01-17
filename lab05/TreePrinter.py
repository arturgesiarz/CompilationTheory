
import AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for ins in self.children:
            ins.printTree(indent)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        print("| " * indent + "Block")
        self.body.printTree(indent)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print("| " * indent + self.assignment)
        self.left_side.printTree(indent + 1)
        self.value.printTree(indent=indent + 1)

    @addToClass(AST.Function)
    def printTree(self, indent=0):
        print("| " * indent + self.fun_name)
        for argument in self.fun_body:
            argument.printTree(indent)

    @addToClass(AST.For)
    def printTree(self, indent=0):
        print("| " * indent + "FOR")
        print("| " * (indent + 1) + self.id)
        print("| " * (indent + 1) + "RANGE")
        self.ne1.printTree(indent=indent + 2)
        self.ne2.printTree(indent=indent + 2)
        self.instruction.printTree(indent=indent + 1)

    @addToClass(AST.While)
    def printTree(self, indent=0):
        print("| " * indent + "WHILE")
        self.expression.printTree(indent=indent + 1)
        self.instruction.printTree(indent=indent + 1)

    @addToClass(AST.If)
    def printTree(self, indent=0):
        print("| " * indent + "IF")
        self.expression.printTree(indent=indent + 1)
        print("| " * indent + "THEN")

        self.instruction1.printTree(indent=indent + 1)
        if self.instruction2:
            print("| " * indent + "ELSE")
            self.instruction2.printTree(indent=indent + 1)

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print("| " * indent + "PRINT")
        for element in self.body:
            element.printTree(indent=indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print("| " * indent + "RETURN")
        if self.instruction:
            self.instruction.printTree(indent=indent + 1)

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print("| " * indent + self.value)

    @addToClass(AST.Id)
    def printTree(self, indent=0):
        print("| " * indent + str(self.name))

    @addToClass(AST.Integer)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.Float)
    def printTree(self, indent=0):
        print("| " * indent + str(self.value))

    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print("| " * indent + "MATRIX")
        for row in self.body:
            row.printTree(indent + 1)

    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print("| " * indent + "VECTOR")
        for val in self.body:
            val.printTree(indent + 1)

    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print("| " * indent + "REF")
        self.var.printTree(indent + 1)
        for val in self.fun_body:
            val.printTree(indent + 1)
            
    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print("| " * indent + "BREAK")
    
    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print("| " * indent + "CONTINUE")

    @addToClass(AST.Expression)
    def printTree(self, indent=0):
        print("| " * indent + self.operator)
        self.left_side.printTree(indent + 1)
        self.right_side.printTree(indent=indent + 1)

    @addToClass(AST.UMinus)
    def printTree(self, indent=0):
        print("| " * indent + '-')
        self.factor.printTree(indent=indent + 1)
    
    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print("| " * indent + 'TRANSPOSE')
        self.factor.printTree(indent=indent + 1)

    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass
