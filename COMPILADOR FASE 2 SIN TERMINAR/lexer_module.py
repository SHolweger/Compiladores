import ply.lex as lex

# Lista de tokens
tokens = (
    'NUMERO', 'DECIMAL', 'BOOLEANO', 'CADENA', 'IDENTIFICADOR',
    'SUMA', 'RESTA', 'MULT', 'DIV',
    'IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL',
    'NEGACION', 'AND', 'OR',
    'PUNTOYCOMA', 'COMA', 'DOSPUNTOS',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER',
    'INICIO', 'SI', 'SINO', 'MIENTRAS', 'REPETIR', 'CAMBIAR',
    'CASO', 'PREDETERMINADO', 'FUNCION', 'REGRESA', 'VERDADERO', 'FALSO'
)

# Palabras reservadas
reservadas = {
    'inicio': 'INICIO',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'repetir': 'REPETIR',
    'cambiar': 'CAMBIAR',
    'caso': 'CASO',
    'predeterminado': 'PREDETERMINADO',
    'funcion': 'FUNCION',
    'regresa': 'REGRESA',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'numero': 'NUMERO',
    'decimal': 'DECIMAL',
    'booleano': 'BOOLEANO',
    'cadena': 'CADENA'
}

# Expresiones regulares para tokens simples
t_SUMA          = r'\+'
t_RESTA         = r'-'
t_MULT          = r'\*'
t_DIV           = r'/'
t_IGUAL         = r'='
t_IGUAL_IGUAL   = r'=='
t_DIFERENTE     = r'!='
t_MAYOR         = r'>'
t_MENOR         = r'<'
t_MAYOR_IGUAL   = r'>='
t_MENOR_IGUAL   = r'<='
t_NEGACION      = r'!'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_PUNTOYCOMA    = r';'
t_COMA          = r','
t_DOSPUNTOS     = r':'
t_PARENIZQ      = r'\('
t_PARENDER      = r'\)'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Comentarios (ignorados)
def t_COMENTARIO(t):
    r'//.*'
    pass

# Manejo de nuevas líneas para actualizar el número de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Cadenas de texto
def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]  # Eliminar las comillas
    return t

# Números decimales
def t_DECIMAL(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Números enteros
def t_NUMERO(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Identificadores y palabras reservadas
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t

# Manejo de errores léxicos
def t_error(t):
    print(f"Carácter ilegal '{t.value[0]}' en la línea {t.lineno}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()

# Función para encontrar la columna de un token
def encontrar_columna(input, token):
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    columna = token.lexpos - last_cr
    return columna

# Función para analizar el código fuente
def analizar_codigo(codigo_fuente):
    lexer.input(codigo_fuente)
    lexer.lexdata = codigo_fuente  # ✅ para calcular bien columnas
    tokens = []
    errores = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens, errores



