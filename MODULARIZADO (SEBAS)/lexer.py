import ply.lex as lex
from tabla_simbolos import verificar_simbolo, verificar_variable_no_inicializada, errores_semanticos, establecer_alcance

# LISTA DE TOKENS
tokens = (
    'INICIO', 'NUMERO', 'DECIMAL', 'BOOLEANO', 'SI', 'SINO', 'MIENTRAS', 'REPETIR', 'REGRESA',
    'IDENTIFICADOR', 'CADENA', 'IGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER', 'PUNTOYCOMA', 'VERDADERO', 'FALSO',
    'AND', 'OR', 'NOT', 'COMA'
)

# PALABRAS RESERVADAS
reserved = {
    'inicio': 'INICIO',
    'numero': 'NUMERO',
    'decimal': 'DECIMAL',
    'booleano': 'BOOLEANO',
    'cadena': 'CADENA',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'repetir': 'REPETIR',
    'regresa': 'REGRESA',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT'
}

# EXPRESIONES REGULARES
t_SUMA = r'\+'
t_RESTA = r'-'
t_MULT = r'\*'
t_DIV = r'/'
t_IGUAL = r'='
t_IGUAL_IGUAL = r'=='
t_DIFERENTE = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_MAYOR_IGUAL = r'>='
t_MENOR_IGUAL = r'<='
t_PARENIZQ = r'\('
t_PARENDER = r'\)'
t_LLAVEIZQ = r'\{'
t_LLAVEDER = r'\}'
t_PUNTOYCOMA = r';'
t_COMA = r','

t_ignore = ' \t'

# LISTA DE TOKENS ADICIONALES
tokens_extraidos = []
errores_lexicos = []

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_CADENA(t):
    r'\".*?\"'
    return t

def t_COMENTARIO_LINEA(t):
    r'\/\/.*'
    pass

def t_COMENTARIO_BLOQUE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Función que maneja errores en el lexer
def t_error(t):
    try:
        columna = encontrar_columna(t.lexer.lexdata, t)
        errores_lexicos.append((f"Error léxico: carácter inesperado '{t.value[0]}'", t.lineno, columna))
        t.lexer.skip(1)
    except AttributeError:
        print("Error léxico sin contexto de lexer.")
        errores_lexicos.append((f"Error léxico sin contexto: '{t.value[0]}'", t.lineno, 0))

def encontrar_columna(lexdata, token):
    """Calcula la columna de un token basado en su posición."""
    linea_inicio = lexdata.rfind('\n', 0, token.lexpos)
    if linea_inicio < 0:
        linea_inicio = -1
    return token.lexpos - linea_inicio

# Función para analizar el código
def analizar_codigo(codigo, lexer):
    global tokens_extraidos, errores_lexicos
    tokens_extraidos = []
    errores_lexicos = []

    lexer.lineno = 1
    lexer.input(codigo)

    while True:
        tok = lexer.token()
        if not tok:
            break
        columna = encontrar_columna(codigo, tok)
        setattr(tok, "column", columna)  # Le agregamos la columna al token
        tokens_extraidos.append(tok)

    return tokens_extraidos, errores_lexicos

def construir_lexer():
    return lex.lex()
