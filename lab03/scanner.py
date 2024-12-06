import ply.lex as lex

# Lista nazw tokenow - zgodnie z dokumentacja
# https://ply.readthedocs.io/en/latest/ply.html
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'for': 'FOR',
    'while': 'WHILE',
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
            'ID',
            'DOTADD', 'DOTSUB', 'DOTMUL', 'DOTDIV',
            'ADDASSIGN', 'SUBASSIGN', 'MULASSIGN', 'DIVASSIGN',
            'LT', 'GT', 'LE', 'GE', 'EQ', 'NE',
            'INTNUM',
            'FLOATNUM',
            'STRING'
        ] + list(reserved.values())

# Definiowanie znakow specjalnych
literals = ['+', '-', '*', '/', '=', '(', ')', '[', ']', '{', '}', ':', '\'', ',', ';']

# Definiowanie operatorow macierzy
t_DOTADD = r'\.\+'
t_DOTSUB = r'\.-'
t_DOTMUL = r'\.\*'
t_DOTDIV = r'\./'

# Definiowanie operatorow przypisania
t_ADDASSIGN = r'\+='
t_SUBASSIGN = r'-='
t_MULASSIGN = r'\*='
t_DIVASSIGN = r'/='

# Definiowanie operatorow relacyjnych
t_LT = r'<'
t_GT = r'>'
t_LE = r'<='
t_GE = r'>='
t_EQ = r'=='
t_NE = r'!='

# Ignorowanie bialych znakow
t_ignore = ' \t'

# Ignorowanie komentarzy
t_ignore_COMMENTS = r'\#.*'


# Reguła dla identyfikatorów, które mogą być zarezerwowanymi słowami lub zmiennymi.
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')  # Check for reserved words
    return t


# Regułę dla liczb zmiennoprzecinkowych
"""
    123.456
    .456
    123e10
    3.14e-5
"""
def t_FLOATNUM(t):
    r'((\d+\.\d*)|(\.\d+))([eE][+-]?\d+)?|(\d+)([eE][+-]?\d+)'
    t.value = float(t.value)
    return t

# Regułę dla liczb calkowitych
def t_INTNUM(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Reguła dla ciągów znaków
def t_STRING(t):
    r'".*?"'
    t.value = str(t.value)
    return t


# Reguła dla nowej linii
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Reguła dla błędów
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


# Budowanie lexera
lexer = lex.lex()