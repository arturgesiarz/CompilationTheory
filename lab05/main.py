import sys
import scanner
import MParser
import TypeChecker

from TreePrinter import TreePrinter
from Interpreter import Interpreter
from Exceptions import ReturnValueException


if __name__ == '__main__':

    try:
        examples = {
            1: "Lab05/Examples/fibonacci.m",
            2: "Lab05/Examples/matrix.m",
            3: "Lab05/Examples/pi.m",
            4: "Lab05/Examples/primes.m",
            5: "Lab05/Examples/sqrt.m",
            6: "Lab05/Examples/triangle.m",  # !!
        }
        filename = sys.argv[1] if len(sys.argv) > 1 else examples[5]
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    parser = MParser.parser
    lexer = scanner.lexer
    ast = parser.parse(file.read(), lexer)
    
    if not MParser.HAVE_ERRORS:
        ast.printTree()

        typeChecker = TypeChecker.TypeChecker()
        typeChecker.visit(ast)  
        
        if TypeChecker.HAVE_ERRORS:
            print("have errors")
        else:
            try:
                ast.accept(Interpreter())
            except ReturnValueException as return_value:
                print("Program return: " + str(return_value))