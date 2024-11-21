import scanner
import ply.yacc as yacc
import AST


# definicja tokenow
tokens = scanner.tokens


# definicja predykcji - określa kolejność wykonywania operacji w wyrażeniach. 
# Określa, które operatory mają wyższy priorytet
start = 'program'
precedence = (
  ('nonassoc', 'IFX'),
  ('nonassoc', 'ELSE'),
  ('right', 'MULASSIGN', 'DIVASSIGN', 'SUBASSIGN', 'ADDASSIGN'),
  ('nonassoc', 'LT', 'GT', 'GE', 'LE', 'EQ', 'NE'),
  ("left", '+', '-'),
  ('left', 'DOTADD', 'DOTSUB'),
  ('left', '*', '/'),
  ('left', 'DOTMUL', 'DOTDIV'),
  ('right', 'UMINUS'),
  ('left', "'"),
)


# Funkcja bledu
def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")
        
        
def p_empty(p):
    """ empty :"""
    p[0] = AST.Empty()


# Reguly gramatyki
def p_program(p):
    """program : instructions_opt"""
    p[0] = p[1]


# Opcjonalny ciag instrukcji
def p_instructions_opt_1(p):
    """instructions_opt : instructions """
    p[0] = p[1]


def p_instructions_opt_2(p):
    """instructions_opt : """
    p[0] = p[1]


# Definiowana jest produkcja dla ciągu instrukcji. 
# Instrukcja może być listą instrukcji lub pojedynczą instrukcją. 
# Reguła p_instructions_1 mówi, że lista instrukcji może składać się z wielu instrukcji, 
# a reguła p_instructions_2 pozwala na pojedynczą instrukcję.
def p_instructions_1(p):
    """instructions : instructions instruction """
    if len(p) == 2:
        p[0] = AST.Instructions(p[1])
        
    elif len(p) == 3:
        p[0] = AST.Instructions(p[2], p[1])


def p_instructions_2(p):
    """instructions : instruction """
    p[0] = AST.Instructions(p[1])


# Określa możliwe formy instrukcji w programie. 
# Instrukcja może być instrukcją systemową (sys_instruction), 
# przypisaniem (assignment), 
# lub blokiem instrukcji otoczonym nawiasami klamrowymi ({ instructions }).
def p_instruction(p):
    """instruction : sys_instruction ';'
                   | assignment ';'
                   | '{' instructions '}' """
    if len(p) == 3:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = p[2]


#  Reguła dla instrukcji RETURN, która zwraca wynik wyrażenia.
def p_sys_instruction_return(p):
    """sys_instruction : RETURN expression """
    p[0] = AST.Return(p[2])


# Reguly definiują instrukcje przerywające (BREAK) 
# i kontynuujące (CONTINUE) w pętli.
def p_sys_instruction_break(p):
    """sys_instruction : BREAK """
    p[0] = AST.Break()


def p_sys_instruction_continue(p):
    """sys_instruction : CONTINUE"""
    p[0] = AST.Continue()


# Definiuje instrukcję PRINT, która wypisuje wartości na ekran.
def p_sys_instruction_print(p):
    """sys_instruction : PRINT print_values """
    p[0] = AST.Print(p[2])


# Określają instrukcje warunkowe IF z możliwością dodania bloku ELSE.
def p_instruction_if(p):
    """instruction : IF '(' condition ')' instruction %prec IFX """
    p[0] = AST.If(p[3], p[5])


def p_instruction_if_else(p):
    """instruction : IF '(' condition ')' instruction ELSE instruction """
    p[0] = AST.IfElse(p[3], p[5], p[7])


# Okreslaja petle for i while
def p_instruction_for(p):
    """instruction : FOR var '=' range instruction """
    p[0] = AST.For(p[2], p[4], p[5])
    

def p_instruction_while(p):
    """instruction : WHILE '(' condition ')' instruction """
    p[0] = AST.While(p[3], p[5])
    

# Określa reguły przypisania wartości do zmiennej (var),
# elementu macierzy (matrix_element) lub 
# elementu wektora (vector_element).
def p_assignment(p):
    """assignment : var assignment_operator expression
                  | matrix_element assignment_operator expression
                  | vector_element assignment_operator expression """
    p[0] = AST.Assignment(p[1], p[2], p[3])


#  Określa różne operatory przypisania 
# (proste = oraz przypisania z operacjami arytmetycznymi).
def p_assignment_operator(p):
    """assignment_operator : '='
                           | ADDASSIGN
                           | SUBASSIGN
                           | MULASSIGN
                           | DIVASSIGN """
    p[0] = p[1]


#  Definiują składnię dla macierzy i wektorów. Macierz składa się z wektorów, a wektor z zmiennych.
def p_matrix(p):
    """matrix : '[' vectors ']' """
    p[0] = p[2]
    

def p_vector(p):
    """vector : '[' variables ']' """
    p[0] = p[2]


def p_vectors(p):
    """vectors : vectors ',' vector
                | vector """
    if len(p) == 4:
        p[0] = AST.Matrix(p[3], p[1])
    
    elif len(p) == 2:
        p[0] = AST.Matrix(p[1])


# Określają funkcje macierzy, takie jak EYE, ONES i ZEROS.
def p_matrix_function(p):
    """matrix_function : function_name '(' INTNUM ')' """
    p[0] = AST.MatrixFunction(p[1], p[3])
    

def p_function_name(p):
    """function_name : EYE
                     | ONES
                     | ZEROS """
    p[0] = p[1]


# Określa zmienną jako identyfikator (ID).
def p_var(p):
    """var : ID """
    p[0] = AST.Variable(p[1])


# Określa liczbę jako liczbę całkowitą (INTNUM) lub zmiennoprzecinkową (FLOATNUM).
def p_number(p):
    """number : INTNUM
              | FLOATNUM """
    p[0] = AST.Number(p[1])


# Określa ciąg znaków (STRING).
def p_string(p):
    """string : STRING """
    p[0] = AST.String(p[1])


# Określa ze zmienna może być:
# liczbą (np. całkowitą lub zmiennoprzecinkową)
# zmienną, której identyfikator został zadeklarowany wcześniej (np. x)
# może to być element tablicy lub macierzy, czyli np. element wektora lub element macierzy, które zostały zdefiniowane poniżej
def p_variable(p):
    """variable : number
                 | var
                 | element """
    p[0] = p[1]


# Określa, jak wygląda element wektora.
# Jest to identyfikator (np. zmienna) typu ID, 
# a następnie indeks w kwadratowych nawiasach [], który jest liczbą całkowitą (INTNUM). 
# Może to być np. vec[0]
def p_vector_element(p):
    """ vector_element : ID "[" INTNUM "]" """
    p[0] = AST.VectorElement(p[1], p[3])


# Określa, jak wygląda element macierzy. 
# Składa się z identyfikatora (ID), który wskazuje na zmienną będącą macierzą, 
# a następnie indeksu w formacie [,], gdzie zarówno pierwszy, jak i drugi indeks są liczbami całkowitymi (INTNUM).
# Może to być np. mat[0, 1]
def p_matrix_element(p):
    """ matrix_element : ID "[" INTNUM "," INTNUM "]" """
    p[0] = AST.MatrixElement(p[1], p[3], p[5])
    
    
# Określa, czym może być element w tym języku. Może to być:
# element wektora.
# element macierzy.
def p_element(p):
    """ element : vector_element
               | matrix_element"""
    p[0] = p[1]
    


# Określa listę zmiennych. Może to być:
# variables ',' variable: Kolejne zmienne oddzielone przecinkami (np. x, y, z).
# variable: Pojedyncza zmienna (np. x).
def p_variables(p):
    """variables : variables ',' variable
                 | variable """
    if len(p) == 4:
        p[0] = AST.Vector(p[3], p[1])
        
    elif len(p) == 2:
        p[0] = AST.Vector(p[1])


# Określa różne formy wyrażeń, które mogą być liczbą, 
# zmienną, 
# macierzą, 
# funkcją macierzy, 
# operacją unarną (uminus),
# transpozycją, 
# elementem macierzy 
# lub wektora.
def p_expression(p):
    """expression : number
                  | var
                  | matrix
                  | matrix_function
                  | uminus
                  | transposition
                  | matrix_element
                  | vector_element """
    p[0] = p[1]


#  Określa operacje binarne (np. dodawanie, odejmowanie, mnożenie) dla wyrażeń.
def p_bin_expression(p):
    """expression : expression '+' expression
                  | expression '-' expression
                  | expression '*' expression
                  | expression '/' expression
                  | expression DOTADD expression
                  | expression DOTSUB expression
                  | expression DOTMUL expression
                  | expression DOTDIV expression """
    p[0] = AST.BinExpr(p[1], p[2], p[3])


# Określa warunki porównania, takie jak równość (EQ), nierówność (NE) i inne.
def p_condition(p):
    """condition : expression EQ expression
                 | expression NE expression
                 | expression LE expression
                 | expression GE expression
                 | expression LT expression
                 | expression GT expression """
    p[0] = AST.Condition(p[1], p[2], p[3])


# Określa operację unarnego minusu.
def p_uminus(p):
    """uminus : '-' expression %prec UMINUS """
    p[0] = AST.Uminus(p[2])


# Określa operację transpozycji dla wyrażeń, która jest reprezentowana przez znak '.
def p_transposition(p):
    """transposition : expression "'" """
    p[0] = AST.Transposition(p[1])


# Określa, co może być przekazane do instrukcji PRINT. Może to być ciąg znaków lub wyrażenie.
def p_print_values(p):
    """print_values : print_values ',' string
                    | print_values ',' expression
                    | string
                    | expression """
    if len(p) == 4:
        p[0] = AST.PrintValues(p[3], p[1])
    elif len(p) == 2:
        p[0] = AST.PrintValues(p[1])

# Tworzymy parser
parser = yacc.yacc(debug=True)
