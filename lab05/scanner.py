import ply.lex as lex

# https://ply.readthedocs.io/en/latest/ply.html
reserved = {
        'if': 'IF',
        'else': 'ELSE',
        'for':'FOR',
        'while':'WHILE',
        'break': 'BREAK',
        'continue': 'CONTINUE',
        'return': 'RETURN',   
        'eye': 'EYE',
        'zeros': 'ZEROS',
        'ones': 'ONES',  
        'print': 'PRINT'
}

# List of token names
tokens = [
    # operatory binare: +, -, *, /
            'ADD',
            'SUB',
            'MUL',
            'DIV',
    # macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
            'DOTADD',
            'DOTSUB',
            'DOTMUL',
            'DOTDIV',
    # operatory relacyjne: <, >, <=, >=, !=, ==  
            'ASSIGN',
            'SUBASSIGN',
            'MULASSIGN',
            'ADDASSIGN',
            'DIVASSIGN',  
    # operatory relacyjne: <, >, <=, >=, !=, ==  
            'G',
            'L',
            'GE',
            'LE',
            'EQ',
            'NEQ',
    # nawiasy: (,), [,], {,}
            'ROUNDOPEN',
            'ROUNDCLOSE',
            'SQUAREOPEN',
            'SQUARECLOSE',
            'CURLYOPEN',
            'CURLYCLOSE',
     # operator zakresu: :
            'RANGE',
    # transpozycja macierzy: '
            'TRANSPOSITION',
    # przecinek i średnik: , ;
            'COMMA',
            'SEMICOLON',  
     # identyfikatory
            'ID',
    # liczby całkowite
            'INTNUM',
    # liczby zmiennoprzecinkowe
            'FLOATNUM',
     # stringi
            'STRING',
        ] + list(reserved.values())

# Definiowanie znakow specjalnych
literals = ['+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';']

# operatory binare: +, -, *, /
t_ADD = r'\+'
t_SUB = r'-'
t_MUL = r'\*'
t_DIV = r'/'

# macierzowe operatory binarne (dla operacji element po elemencie): .+, .-, .*, ./
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTDIV = r'\./'
t_DOTMUL = r'\.\*'

# operatory przypisania: =, +=, -=, *=, /=
t_ASSIGN = r'\='
t_SUBASSIGN = r'\-\='
t_MULASSIGN = r'\*\='
t_ADDASSIGN = r'\+\='
t_DIVASSIGN = r'\/\='

# operatory relacyjne: <, >, <=, >=, !=, == 
t_G = r'\<'
t_L = r'\>'
t_GE = r'\<\='
t_LE = r'\>\='
t_EQ = r'\=\='
t_NEQ = r'\!\='

# nawiasy: (,), [,], {,}
t_ROUNDOPEN = r'\('
t_ROUNDCLOSE = r'\)'
t_SQUAREOPEN = r'\['
t_SQUARECLOSE = r'\]'
t_CURLYOPEN = r'\{'
t_CURLYCLOSE = r'\}'

# operator zakresu: :
t_RANGE = r'\:' 

# transpozycja macierzy ': 
t_TRANSPOSITION = r'\''
  
# przecinek i średnik: ,  ;
t_COMMA = r'\,' 
t_SEMICOLON = r'\;'

# string zawierający ignorowane znaki (spacje i taby)
t_ignore = ' \t'
t_ignore_COMMENT = r'\#.*'

# identyfikatory (pierwszy znak identyfikatora to litera lub znak _, w kolejnych znakach mogą dodatkowo wystąpić cyfry)     
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t

#liczby zmiennoprzecinkowe
def t_FLOATNUM(t):
    r'-?((\d*\.\d+E-?\d+)|(\d+\.\d*E-?\d+)|(\d*\.\d+)|(\d+\.\d*))'

    if t.value[0] == '-':
        t.value = float(t.value[1:])
        t.value *=-1
    else:
        t.value = float( t.value)
    return t

# liczby całkowite
def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# stringi
def t_STRING(t):
    r'"[^"]*"'
    t.value = t.value[1:len(t.value) - 1]
    return t

# defniujemy zasadę umożliwiającą numerowanie linii
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# zasada obsługująca błędy
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

class Lexer:
    def __init__(self):
        self.tokens = []
        self.lexer = lex.lex()

    def tokenize(self, data):
        self.lexer.input(data)
        self.tokens = []
        token = self.lexer.token()
        
        while token :
            self.tokens.append(token)
            token = self.lexer.token()

    def tokenToStr(self,token):
        return str(token.lineno)+ " " + str(token.type) + "(" +str(token.value) + ")" 

    def getTokens(self):
        return self.tokens[:]

# Budowanie lexera  
lexer = Lexer().lexer
