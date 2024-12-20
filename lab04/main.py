import sys
import scanner
import MParser
from TreePrinter import TreePrinter
from TypeChecker import TypeChecker

if __name__ == '__main__':
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "Lab04/Examples/opers.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = MParser.parser
    lexer = scanner.lexer
    ast = parser.parse(file.read(), lexer)
    
    if not MParser.HAVE_ERRORS:
        ast.printTree()
        typeChecker = TypeChecker()
        typeChecker.visit(ast)
