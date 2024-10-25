import sys
import scanner

if __name__ == '__main__':

    # Otwierania pliku
    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "lab01/example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    # Wczytywanie pliku do lexera
    text = file.read()
    lexer = scanner.lexer
    lexer.input(text)
    
    # Tokenizacja odczytanego kodu i zapis do pliku
    with open('lab01/output.txt', 'w') as output_file:
      while True:
        tok = lexer.token()
        if not tok:
            break  # No more input
        print(f'{tok.lineno}: {tok.type}({tok.value})', file=output_file)
          