import ply.lex as lex
import html_gen
#from parser import ruta_archivo

# LISTA DE TOKENS
tokens = (
    'INICIO', 'NUMERO', 'DECIMAL', 'BOOLEANO', 'SI', 'SINO', 'MIENTRAS', 'REPETIR', 'REGRESA',
    'IDENTIFICADOR', 'CADENA', 'IGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER', 'PUNTOYCOMA', 'VERDADERO', 'FALSO'
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
    'falso': 'FALSO'
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


t_ignore = ' \t'

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

def t_COMENTARIO_LINEA(t):
    r'\/\/.*'
    pass 

def t_COMENTARIO_BLOQUE(t):
    r'/\*[\s\S]*?\*/'
    t.lexer.lineno += t.value.count('\n')
    pass 

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

def encontrar_columna(input, token):
    # Buscar el último salto de línea antes del token
    last_cr = input.rfind('\n', 0, token.lexpos)
    if last_cr < 0:
        return token.lexpos + 1  # Si no hay salto de línea previo, la columna es la posición del token + 1
    return (token.lexpos - last_cr)

def analizar_codigo(codigo):
    lexer.lineno = 1
    lexer.input(codigo)
    global tokens_extraidos, errores_lexicos
    tokens_extraidos = []
    errores_lexicos = []

    while tok := lexer.token():
        tok.column = encontrar_columna(codigo, tok)  # Agregar columna al token 
        tokens_extraidos.append(tok)
    return tokens_extraidos

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print("Archivo leido correctamente.\n")
        print("\n----- Codigo leido desde el archivo -----\n")
        print(contenido)
        analizar_codigo(contenido)
    except FileNotFoundError:
        print("Error: No se encontro el archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

# Ruta del código fuente
ruta_archivo = "codigo_fuente.txt"
#ruta_archivo = "COMPILADOR Proyecto\codigo_fuente.txt"
# ESTO ES PARA SEBAS EN MAC XD
#ruta_archivo = "COMPILADOR Proyecto/codigo_fuente.txt"
leer_archivo(ruta_archivo)