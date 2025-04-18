import ply.lex as lex
import html_gen

# LISTA DE TOKENS
tokens = (
    'INICIO', 'NUMERO', 'DECIMAL', 'BOOLEANO', 'SI', 'SINO', 'MIENTRAS', 'REPETIR', 'REGRESA',
    'IDENTIFICADOR', 'CADENA', 'IGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER', 'PUNTOYCOMA', 'VERDADERO', 'FALSO',
    'FUNCION', 'COMA', 'AND', 'OR', 'NEGACION', 'CAMBIAR', 'CASO', 'DOSPUNTOS', 'PREDETERMINADO', 'COMENTARIO_LINEA', 'COMENTARIO_BLOQUE'
)

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
    'funcion': 'FUNCION',
    'cambiar': 'CAMBIAR',
    'caso': 'CASO',
    'predeterminado': 'PREDETERMINADO',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE',
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
t_COMA = r','           # Separador de parámetros o argumentos
# Expresiones regulares para los nuevos tokens
t_NEGACION = r'!'
t_ignore =  ' \t'
t_DOSPUNTOS = r':'
t_COMENTARIO_LINEA = r'\/\/.*'
t_COMENTARIO_BLOQUE = r'/\*[\s\S]*?\*/'

tokens_extraidos = []
errores_lexicos = []

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    # print(f"💡 IDENTIFICADOR detectado: {t.value}")
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
    t.value = t.value[1:-1]  # Remover las comillas al inicio y al final
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)  # Incrementar el número de línea según los saltos de línea

def t_error(t):
    col = encontrar_columna(t.lexer.lexdata, t)
    if col == -1:
        col = t.lexpos - t.lexer.lexdata.rfind('\n', 0, t.lexpos) - 1
    errores_lexicos.append((f"Error lexico: Caracter inesperado '{t.value[0]}'", t.lineno, col))
    t.lexer.skip(1)
    

lexer = lex.lex()

def encontrar_columna(input, token): # Encuentra la columna del token
    last_cr = input.rfind('\n', 0, token.lexpos) # Encuentra el último salto de línea antes del token
    if last_cr < 0: # Si no hay salto de línea previo, la columna es la posición del token
        last_cr = -1  # Si no hay salto de línea previo, la columna es la posición del token
    return (token.lexpos - last_cr) # -1 para ajustar a 0-indexed


def analizar_codigo(codigo):
    lexer.lineno = 1
#    lexer.lexcol = 1
    lexer.input(codigo)
    global tokens_extraidos, errores_lexicos
    tokens_extraidos = []
    errores_lexicos = []

    while tok := lexer.token():
        tok.column = encontrar_columna(codigo, tok)  # Agregar columna al token 
        print(f"Token: {tok.type}, Valor: {tok.value}, Línea: {tok.lineno}, Columna: {tok.column}")
        tokens_extraidos.append(tok)
    return tokens_extraidos, errores_lexicos