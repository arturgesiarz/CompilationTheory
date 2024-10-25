
from sly import Lexer

class MatrixLexer(Lexer):
    tokens = {
        ID, INTNUM, FLOATNUM,
        EYE, ZEROS, ONES,
        PRINT, IF, ELSE, FOR, WHILE,
        BREAK, CONTINUE, RETURN,
        ASSIGN, ADD, SUB, MUL, DIV,
        DOTADD, DOTSUB, DOTMUL, DOTDIV,
        LPAREN, RPAREN, LBRACE, RBRACE,
        LBRACK, RBRACK, COLON, SEMICOLON,
        COMMA, TRANSPOSE,
        NEQ, EQ, LT, GT, LEQ, GEQ,
        STRING
    }

    ignore = ' \t'

    # Komentarze
    @_(r'#.*')
    def ignore_comment(self, t):
        pass

    # Zdefiniowane leksemy
    ID = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INTNUM = r'\d+'
    FLOATNUM = r'\d+\.\d*([eE][-+]?\d+)?'  # Ulepszona obsługa liczb zmiennoprzecinkowych
    STRING = r'"([^"\\]*(\\.[^"\\]*)*)"'  # Rozpoznawanie ciągów znakowych

    EYE = r'eye'
    ZEROS = r'zeros'
    ONES = r'ones'
    PRINT = r'print'
    IF = r'if'
    ELSE = r'else'
    FOR = r'for'
    WHILE = r'while'
    BREAK = r'break'
    CONTINUE = r'continue'
    RETURN = r'return'

    ASSIGN = r'='
    ADD = r'\+'
    SUB = r'-'
    MUL = r'\*'
    DIV = r'/'

    DOTADD = r'\.\+'
    DOTSUB = r'\.-'
    DOTMUL = r'\.\*'
    DOTDIV = r'\./'

    LPAREN = r'\('
    RPAREN = r'\)'
    LBRACE = r'\{'
    RBRACE = r'\}'
    LBRACK = r'\['
    RBRACK = r'\]'
    COLON = r':'
    SEMICOLON = r';'
    COMMA = r','
    TRANSPOSE = r'\''

    NEQ = r'!='
    EQ = r'=='
    LT = r'<'
    GT = r'>'
    LEQ = r'<='
    GEQ = r'>='

    # Funkcja do zwracania tokenów
    def error(self, t):
        print(f'Niepoprawny token: {t.value[0]} w linii {t.lineno}')
        self.index += 1

if __name__ == '__main__':
    lexer = MatrixLexer()
    
    with open('lab01/example.txt', 'r') as file:
        code = file.read()
        
    with open('lab01/output.txt', 'w') as output_file:
        # Tokenizacja odczytanego kodu i zapis do pliku
        for token in lexer.tokenize(code):
            output_file.write(f'{token}\n')  # Zapisz każdy token w nowej linii
