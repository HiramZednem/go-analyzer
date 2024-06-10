import ply.yacc as yacc
from lex import tokens

# Definir las reglas gramaticales

def p_program(p):
    'program : PACKAGE IDENTIFIER SEMICOLON import_decls func_decls'
    p[0] = ('program', p[2], p[4], p[5])

def p_import_decls(p):
    'import_decls : IMPORT STRING SEMICOLON'
    p[0] = ('import', p[2])

def p_func_decls(p):
    'func_decls : FUNC MAIN LPAREN RPAREN LBRACE stmt_list RBRACE'
    p[0] = ('func', 'main', p[6])

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
                 | stmt'''
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = [p[1]]

def p_stmt(p):
    'stmt : FMT_PRINTLN LPAREN STRING RPAREN SEMICOLON'
    p[0] = ('print', p[3])

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}'")
        print(f"Type: {p.type}")
        print(f"Line: {p.lineno}")
    else:
        print("Syntax error at EOF")


# Construir el analizador sintáctico
parser = yacc.yacc()
