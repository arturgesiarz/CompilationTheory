import AST

def addToClass(cls):
    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    
    return decorator

class TreePrinter:
    
    @classmethod
    def indent(self, length):
        return ''.join('|   ' * length)

    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)
    
    # wyrażenia binarne
    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)
        
        
    # wyrazanie relacyjne   
    @addToClass(AST.Condition)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)
    
    @addToClass(AST.Number)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + str(self.value))
    
    @addToClass(AST.String)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.value)
    
    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.name)
    
    
    # instrukcje warunkowe if-else
    @addToClass(AST.If)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.indent(indent) + 'THEN')
        self.instruction.printTree(indent + 1)
    
    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'IF')
        self.condition.printTree(indent + 1)
        print(TreePrinter.indent(indent) + 'THEN')
        self.if_instruction.printTree(indent + 1)
        print(TreePrinter.indent(indent) + 'ELSE')
        self.else_instruction.printTree(indent + 1)
    
    
    # pętle: while oraz for
    @addToClass(AST.While)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'WHILE')
        self.condition.printTree(indent + 1)
        self.instruction.printTree(indent + 1)
        
    @addToClass(AST.For)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'FOR')
        self.var.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.instruction.printTree(indent + 1)
    
    @addToClass(AST.Range)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'RANGE')
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
    
    
    # instrukcje break, continue oraz return    
    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'BREAK')
    
    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'CONTINUE')
    
    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'RETURN')
        self.value.printTree(indent + 1)
        
    # instrukcje print
    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'PRINT')
        self.values.printTree(indent + 1)
    
    @addToClass(AST.PrintValues)
    def printTree(self, indent=0):
        for val in self.values:
            val.printTree(indent)
            
            
    # instrukcje zlozone
    @addToClass(AST.Instructions)
    def printTree(self, indent=0):
        for instruction in self.instructions:
            instruction.printTree(indent)
            
    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.operator)
        self.variable.printTree(indent + 1)
        self.expression.printTree(indent + 1)
    
    @addToClass(AST.Uminus)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'UMINUS')
        self.expression.printTree(indent + 1)
    
    @addToClass(AST.Transposition)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'TRANSPOSE')
        self.matrix.printTree(indent + 1)
        
        
    # tablice
    @addToClass(AST.Matrix)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'MATRIX')
        for vector in self.matrix:
            vector.printTree(indent + 1)
    
    @addToClass(AST.MatrixElement)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'MATRIX ELEMENT')
        print(TreePrinter.indent(indent + 1) + self.id)
        print(TreePrinter.indent(indent + 1) + str(self.row_idx))
        print(TreePrinter.indent(indent + 1) + str(self.col_idx))
    
    @addToClass(AST.MatrixFunction)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + self.function_name)
        print(TreePrinter.indent(indent + 1) + self.function_arg)
        
    @addToClass(AST.Vector)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'VECTOR')
        for elem in self.vector:
            elem.printTree(indent + 1)
            
    @addToClass(AST.VectorElement)
    def printTree(self, indent=0):
        print(TreePrinter.indent(indent) + 'VECTOR ELEMENT')
        self.id.printTree(indent + 1)
        print(TreePrinter.indent(indent + 1) + str(elf.index))
        
        
    @addToClass(AST.Error)
    def printTree(self, indent=0):
        pass

