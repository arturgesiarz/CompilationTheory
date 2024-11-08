import sys
import scanner
import Mparser

if __name__ == '__main__':

    # otwieranie pliku
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab02/data/example1.m"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)
    
    parser = Mparser.parser
    text = file.read()
    parser.parse(text, lexer=scanner.lexer)
          