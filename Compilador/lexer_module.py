#Lexer_module.py
import ply.lex as lex

# -------------------------------------------------------------------------
# Definición de tokens organizados por categorías
# -------------------------------------------------------------------------
tokens_literales = (
    'NUMERO', 'DECIMAL', 'CADENA', 'IDENTIFICADOR'
)

tokens_aritmeticos = (
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD'
)

tokens_asignacion = (
    'IGUAL', 'SUMA_IGUAL', 'RESTA_IGUAL', 'MULT_IGUAL', 'DIV_IGUAL'
)

tokens_comparacion = (
    'IGUAL_IGUAL', 'DIFERENTE', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'
)

tokens_logicos = (
    'NEGACION', 'AND', 'OR'
)

tokens_delimitadores = (
    'PUNTOYCOMA', 'COMA', 'DOSPUNTOS', 'PUNTO',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER',
    'CORCHETEIZQ', 'CORCHETEDER'
)

reservadas = {
    'inicio': 'INICIO',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'repetir': 'REPETIR',
    'hasta': 'HASTA',
    'para': 'PARA',
    'funcion': 'FUNCION',
    'regresa': 'REGRESA',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'mostrar': 'MOSTRAR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    # Tipos
    'numero': 'NUMERO',
    'decimal': 'DECIMAL',
    'booleano': 'BOOLEANO',
    'cadena': 'CADENA',
}

tokens = list(set(
    tuple(reservadas.values()) +
    tokens_literales + tokens_aritmeticos +
    tokens_asignacion + tokens_comparacion +
    tokens_logicos + tokens_delimitadores
))

# -------------------------------------------------------------------------
# Reglas de expresiones regulares
# -------------------------------------------------------------------------
t_SUMA_IGUAL    = r'\+='
t_RESTA_IGUAL   = r'-='
t_MULT_IGUAL    = r'\*='
t_DIV_IGUAL     = r'/='

t_SUMA          = r'\+'
t_RESTA         = r'-'
t_MULT          = r'\*'
t_DIV           = r'/'
t_MOD           = r'%'

t_IGUAL         = r'='
t_IGUAL_IGUAL   = r'=='
t_DIFERENTE     = r'!='
t_MAYOR_IGUAL   = r'>='
t_MENOR_IGUAL   = r'<='
t_MAYOR         = r'>'
t_MENOR         = r'<'

t_NEGACION      = r'!'
t_AND           = r'&&'
t_OR            = r'\|\|'

t_PUNTOYCOMA    = r';'
t_COMA          = r','
t_DOSPUNTOS     = r':'
t_PUNTO         = r'\.'
t_PARENIZQ      = r'\('
t_PARENDER      = r'\)'
t_LLAVEIZQ      = r'\{'
t_LLAVEDER      = r'\}'
t_CORCHETEIZQ   = r'\['
t_CORCHETEDER   = r'\]'

t_ignore = ' \t'

def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

def t_COMENTARIO(t):
    r'//.*'
    pass

def t_CADENA(t):
    r'"([^\\\n]|(\\.))*?"'
    t.value = t.value[1:-1]
    return t

def t_DECIMAL(t):
    r'\d+\.\d+'  
    t.value = float(t.value)
    return t

def t_NUMERO(t):
    r'\d+' 
    t.value = int(t.value)
    return t

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*' 
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    from lexer_module import encontrar_linea, encontrar_columna
    linea = encontrar_linea(t.lexer.lexdata, t)
    columna = encontrar_columna(t.lexer.lexdata, t)
    mensaje = f"Error Léxico: Carácter ilegal '{t.value[0]}'"
    t.lexer.errores.append((mensaje, linea, columna))
    t.lexer.skip(1)

def encontrar_columna(input_text, token):
    try:
        last_cr = input_text.rfind('\n', 0, token.lexpos)
        if last_cr < 0: last_cr = -1
        return token.lexpos - last_cr
    except:
        return 0

def encontrar_linea(input_text, token):
    try:
        return input_text.count('\n', 0, token.lexpos) + 1
    except:
        return 1

lexer = lex.lex()

def analizar_codigo(codigo_fuente):
    lexer.lineno = 1
    lexer.input(codigo_fuente)
    lexer.lexdata = codigo_fuente
    lexer.errores = []
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tok.lineno = encontrar_linea(lexer.lexdata, tok)  # ya existe en PLY, solo reforzamos
        tok.column = encontrar_columna(lexer.lexdata, tok)  # importante: usar 'column'
        tokens.append(tok)
    return tokens, lexer.errores
