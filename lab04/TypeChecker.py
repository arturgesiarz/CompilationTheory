import AST
import SymbolTable

from type_table import *

nested_loops_number = 0

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, AST.Node):
                            self.visit(item)
                elif isinstance(child, AST.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):
    def __init__(self):
        self.symbol_table = SymbolTable(None, 'god why')

    def visit_Expression(self, node):
        symbol1 = self.visit(node.left_side)
        symbol2 = self.visit(node.right_side)
        op = node.operator

        if symbol1 is None or symbol2 is None:
            print('Can\'t execute operation with undeclared variables in line {}'.format(node.line_number))
            return None

        result_symbol = get_new_symbol(op, symbol1, symbol2)
        
        if isinstance(result_symbol, str):
            print("{} in line {}".format(result_symbol, node.line_number))
            return None
        
        return result_symbol


    def visit_Assignment(self, node):
        ex_symbol = self.visit(node.value)

        if ex_symbol is None:
            print('Right side value in assigment doesn\'t exist in line {}'.format(node.line_number))
            return None

        if node.assignment == '=':
            if isinstance(node.left_side, AST.Range):
                left_side_symbol = self.visit(node.left_side)
                if left_side_symbol:
                    left_side_type = left_side_symbol.type
                    if left_side_type != ex_symbol.type:
                        print("Can't assign {} of type {} to {} of type {} in line {}".format(ex_symbol.type_name, ex_symbol.type, left_side_symbol.type_name, left_side_type, node.line_number))
            else:
                ex_symbol.name = node.left_side.name
                self.symbol_table.put(node.left_side.name, ex_symbol)
        else:
            left_side_symbol = self.visit(node.left_side)
            if left_side_symbol:
                result_symbol = get_new_symbol(node.assignment[0], left_side_symbol, ex_symbol)

                if isinstance(result_symbol, str):
                    print("{} in line {}".format(result_symbol, node.line_number))
                    return None
                ex_symbol.name = node.left_side.name
                self.symbol_table.put(node.left_side.name, ex_symbol)
                return result_symbol


    def visit_Integer(self, node):
        return VariableSymbol('', 'int')


    def visit_Float(self, node):
        return VariableSymbol('', 'float')


    def visit_Vector(self, node):
        types = []
        for val in node.body:
            visited_val = self.visit(val)
            if not isinstance(visited_val, VariableSymbol):
                print('Element of Vector is not a Variable in line {}'.format(node.line_number))
                return None
            types.append(visited_val.type)
        new_type = vector_type(types)
        if new_type:
            return VectorSymbol('', new_type, len(node.body))
        print('Conflicting types in Vector in line {}'.format(node.line_number))
        return None


    def visit_Matrix(self, node):
        types = []
        size = None
        for i in range(len(node.body)):
            val = node.body[i]
            visited_val = self.visit(val)
            types.append(visited_val.type)
            if size:
                if size != visited_val.size:
                    print('Conflicting sizes of Vectors in Matrix in line {}'.format(node.line_number))
                    return None
            else:
                size = visited_val.size
            if not isinstance(visited_val, VectorSymbol):
                print('Element of matrix is not a Vector in line {}'.format(node.line_number))
                return None

        new_type = vector_type(types)
        if new_type:
            return MatrixSymbol('', new_type, (len(node.body), size))
        print('Conflicting types of Vectors in Matrix in line {}'.format(node.line_number))
        return None


    def visit_Function(self, node):
        symbols = []
        for arg in node.fun_body:
            symbols.append(self.visit(arg))

        if node.fun_name == 'ones' or node.fun_name == 'zeros' or node.fun_name == 'eye':
            if len(symbols) > 2 or len(symbols) < 1:
                print('Bad number of arguments for function {} in line {}'.format(node.fun_name, node.line_number))
                return None
            for sym in symbols:
                if sym.type != 'int':
                    print('Bad argument for function {} in line {}'.format(node.fun_name, node.line_number))
                    return None
            if len(symbols) == 2:
                return MatrixSymbol('', 'int', (node.fun_body[0].value, node.fun_body[1].value))
            return MatrixSymbol('', 'int', (node.fun_body[0].value, node.fun_body[0].value))

        print('Function {} is not defined in line {}'.format(node.fun_name, node.line_number))
        return None

    def visit_Id(self, node):
        tmp = self.symbol_table.get(node.name)
        if tmp is None:
            print("Variable {} referenced before assignment in line {}".format(node.name, node.line_number))
        return tmp

    def visit_Block(self, node):
        self.symbol_table = self.symbol_table.pushScope('new')
        self.visit(node.body)
        self.symbol_table = self.symbol_table.popScope()

    def visit_Range(self, node):
        var = self.symbol_table.get(node.var.name)

        if var is None:
            return print("Variable undefined in line {}".format(node.line_number))
        if isinstance(var, MatrixSymbol):

            if len(node.fun_body) != 2:
                return print("Invalid arguments number in line {}".format(node.line_number))
            if not 0 <= node.fun_body[0].value < var.size[0] or not 0 <= node.fun_body[1].value < var.size[1]:
                return print("Out of range in line {0}".format(node.line_number))
            return VariableSymbol("Matrix", var.type)
        if isinstance(var, VectorSymbol):
            if len(node.fun_body) != 1:
                return print("Invalid arguments number in line {}".format(node.line_number))
            if 0 > node.fun_body[0].value >= var.size :
                return print("Out of range")
            return VariableSymbol("Vector", var.type)
        return print("Can't use range on {} in line {}".format(var.type_name, node.line_number))


    def visit_String(self, node):
        return VariableSymbol("Variable", "string")

    def visit_For(self, node):
        self.symbol_table = self.symbol_table.pushScope('new')
        
        ex_symbol = VariableSymbol('Variable', 'int')
        
        self.symbol_table.put(node.id, ex_symbol)
        self.visit(node.ne1)
        self.visit(node.ne2)
        
        global nested_loops_number
        nested_loops_number += 1
        
        self.visit(node.instruction)
        nested_loops_number -= 1
        self.symbol_table = self.symbol_table.popScope()

    def visit_While(self, node):
        self.visit(node.expression)
        global nested_loops_number
        nested_loops_number += 1
        self.visit(node.instruction)
        nested_loops_number -= 1

    def visit_FlowKeyword(self, node):
        if nested_loops_number == 0:
            print(node.value + " outside loop in line {}".format(node.line_number))

    def visit_Return(self, node):
        expresion_result = self.visit(node.instruction)
        if expresion_result == None:
            print("Return: undefinded value in line {}".format(node.line_number) )

    def visit_Print(self, node):
        for element in node.body:
            self.visit(element)

    def visit_If(self,node):
        self.visit(node.expression)
        self.visit(node.instruction1)
        if node.instruction2:
            self.visit(node.instruction2)

    def visit_Transposition(self, node):
        ex_symbol = self.visit(node.factor)
        if not isinstance(ex_symbol, MatrixSymbol):
            print("Operator \"'\" (transposition) can only be used with matrices in line {}".format(node.line_number))
            return None

        ex_symbol.size = (ex_symbol.size[1], ex_symbol.size[0])
        self.symbol_table.put(ex_symbol.name, ex_symbol)
        return ex_symbol

    def visit_UMinus(self, node):
        ex_symbol = self.visit(node.factor)
        if isinstance(ex_symbol, VectorSymbol):
            print('Unary minus operator \"-\" can\'t be used with Vector in line {}'.format(node.line_number))
            return None
        return ex_symbol