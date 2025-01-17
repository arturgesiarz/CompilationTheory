
class Symbol(object):
    pass

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.type_name = 'Variable'

class VectorSymbol(Symbol):
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size
        self.type_name = 'Vector'


class MatrixSymbol(Symbol):
    def __init__(self, name, type, size):
        self.name = name
        self.type = type
        self.size = size
        self.type_name = 'Matrix'


class SymbolTable(object):
    def __init__(self, parent, name):
        self.parent = parent
        self.name = name
        self.dict = {}

    def put(self, name, symbol):
        self.dict[name] = symbol

    def get(self, name):
        if name in self.dict:
            return self.dict[name]
        else:
            if self.parent:
                return self.parent.get(name)
        return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        return SymbolTable(self, '...')

    def popScope(self):
        return self.parent
