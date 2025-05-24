#lexer_module.py
import ply.lex as lex

# ------------------------------------------------------------------------------
# Definición de tokens organizados por categorías
# ------------------------------------------------------------------------------
# Literales y nombres
tokens_literales = (
    'NUMERO', 'DECIMAL', 'CADENA', 'IDENTIFICADOR'
)

# Operadores aritméticos
tokens_aritmeticos = (
    'SUMA', 'RESTA', 'MULT', 'DIV', 'MOD'
)

# Operadores de asignación (incluye asignación simple '=' y compuestos)
tokens_asignacion = (
    'IGUAL', 'SUMA_IGUAL', 'RESTA_IGUAL', 'MULT_IGUAL', 'DIV_IGUAL'
)

# Operadores de comparación
tokens_comparacion = (
    'IGUAL_IGUAL', 'DIFERENTE', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'
)

# Operadores lógicos
tokens_logicos = (
    'NEGACION', 'AND', 'OR'
)

# Delimitadores y puntuación
tokens_delimitadores = (
    'PUNTOYCOMA', 'COMA', 'DOSPUNTOS', 'PUNTO',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER', 'CORCHETEIZQ', 'CORCHETEDER'
)

# Palabras reservadas (mapeo a tokens)
reservadas = {
    'inicio': 'INICIO',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'repetir': 'REPETIR',
    'hasta': 'HASTA',
    'para': 'PARA',
    'cambiar': 'CAMBIAR',
    'caso': 'CASO',
    'predeterminado': 'PREDETERMINADO',
    'funcion': 'FUNCION',
    'regresa': 'REGRESA',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO',
    'menu': 'MENU',
    'mostrar': 'MOSTRAR',
    'break': 'BREAK',
    'continue': 'CONTINUE',
    # Tipos como literales de palabra reservada
    'numero': 'NUMERO',
    'decimal': 'DECIMAL',
    'booleano': 'BOOLEANO',
    'cadena': 'CADENA',
}

# tokens reserva como tupla
tokens_reservadas = tuple(reservadas.values())

# Construcción de la lista final de tokens
tokens = list(set(tokens_reservadas+tokens_literales + tokens_aritmeticos + tokens_asignacion + tokens_comparacion +tokens_logicos+tokens_delimitadores))

# ------------------------------------------------------------------------------
# Reglas de expresión regular para tokens simples
# ------------------------------------------------------------------------------
# Comentario multilínea (se ignora y actualiza líneas)
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario de línea (ignorado)
def t_COMENTARIO(t):
    r'//.*'
    pass

# Operadores de asignación compuestos

t_SUMA_IGUAL    = r'\+='    
t_RESTA_IGUAL   = r'-='    
t_MULT_IGUAL    = r'\*='    
t_DIV_IGUAL     = r'/='    

# Operadores aritméticos simples
t_SUMA          = r'\+'  
t_RESTA         = r'-'   
t_MULT          = r'\*'  
t_DIV           = r'/'   
t_MOD           = r'%'   

# Comparación y asignación simple
t_IGUAL         = r'='   
t_IGUAL_IGUAL   = r'=='  
t_DIFERENTE     = r'!='  
t_MAYOR_IGUAL   = r'>='  
t_MENOR_IGUAL   = r'<='  
t_MAYOR         = r'>'   
t_MENOR         = r'<'   

# Operadores lógicos
t_NEGACION      = r'!'   
t_AND           = r'&&'  
t_OR            = r'\|\|'   

# Delimitadores y puntuación
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

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Nuevas líneas para el conteo de líneas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ------------------------------------------------------------------------------
# Reglas de tokens con acción
# ------------------------------------------------------------------------------
# Cadenas de texto (elimina comillas)
def t_CADENA(t):
    r'\"([^\\\n]|(\\.))*?\"'
    t.value = t.value[1:-1]
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
# Asigna token de palabra reservada si coincide (case-insensitive)
def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value.lower(), 'IDENTIFICADOR')
    return t

# Manejo de errores léxicos
# Manejo de errores léxicos
def t_error(t):
    linea = encontrar_linea(t.lexer.lexdata, t)
    columna = encontrar_columna(t.lexer.lexdata, t)
    mensaje = f"Carácter ilegal '{t.value[0]}' en la línea {linea}, columna {columna}"
    print(mensaje)
    
    if not hasattr(t.lexer, 'errores'):
        t.lexer.errores = []
    
    t.lexer.errores.append({
        'tipo': 'Léxico',
        'descripcion': mensaje,
        'linea': linea,
        'columna': columna
    })
    t.lexer.skip(1)

# ------------------------------------------------------------------------------
# Construcción del lexer y funciones auxiliares
# ------------------------------------------------------------------------------
lexer = lex.lex()

def encontrar_columna(input_text, token):
    last_cr = input_text.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        last_cr = -1
    return token.lexpos - last_cr


def encontrar_linea(input_text, token):
    return input_text.count('\n', 0, token.lexpos) + 1

# Función principal de análisis de código
def analizar_codigo(codigo_fuente):
    lexer.lineno = 1
    lexer.input(codigo_fuente)
    lexer.lexdata = codigo_fuente
    tokens = []
    errores = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tok.line = encontrar_linea(lexer.lexdata, tok)
        tok.column = encontrar_columna(lexer.lexdata, tok)
        tokens.append(tok)
    return tokens, errores
