import ply.lex as lex

# Lista de tokens
tokens = [
    'IDENTIFIER', 'NUMBER', 'STRING',
    'PLUS', 'EQUALS', 'SEMICOLON',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'DOT'
]

# Palabras reservadas
reserved = {
    'package': 'PACKAGE',
    'import': 'IMPORT',
    'func': 'FUNC',
    'main': 'MAIN',
    'fmt.Println': 'FMT_PRINTLN'
}

tokens += list(reserved.values())

# Reglas de expresiones regulares para tokens simples
t_PLUS = r'\+'
t_EQUALS = r'='
t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'

# Regla para números
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Regla para identificadores y palabras reservadas
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFIER')  # Verifica palabras reservadas
    return t

# Regla para strings
def t_STRING(t):
    r'\"([^\\\n]|(\\.))*?\"'
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de nuevas líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Manejo de errores
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Construir el analizador léxico
lexer = lex.lex()
