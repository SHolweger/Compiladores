import ply.lex as lex
import html_gen

# LISTA DE TOKENS
tokens = (
    'INICIO', 'NUMERO', 'DECIMAL', 'BOOLEANO', 'SI', 'SINO', 'MIENTRAS', 'REPETIR', 'REGRESA',
    'IDENTIFICADOR', 'CADENA', 'IGUAL', 'SUMA', 'RESTA', 'MULT', 'DIV',
    'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL', 'IGUAL_IGUAL', 'DIFERENTE',
    'PARENIZQ', 'PARENDER', 'LLAVEIZQ', 'LLAVEDER', 'PUNTOYCOMA', 'VERDADERO', 'FALSO'
)

# PALABRAS CLAVE RESERVADAS
reserved = {
    'inicio': 'INICIO',
    'numero': 'NUMERO',
    'decimal': 'DECIMAL',
    'booleano': 'BOOLEANO',
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'repetir': 'REPETIR',
    'regresa': 'REGRESA',
    'verdadero': 'VERDADERO',
    'falso': 'FALSO'
}

# EXPRESIONES REGULARES PARA TOKENS SIMPLES
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

def t_IDENTIFICADOR(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'IDENTIFICADOR')
    return t

# NUMEROS DECIMALES ANTES DE ENTEROS
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

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

def t_error(t):
    print(f"Error lexico: Caracter inesperado '{t.value[0]}' en la linea {t.lineno}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

def analizar_codigo(codigo):
    lexer.input(codigo)
    tokens_extraidos = []
    while tok := lexer.token():
        tokens_extraidos.append(tok)
    html_gen(tokens_extraidos)  # Llamamos a la función de generación de HTML 
    return tokens_extraidos

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.readlines()
            codigo = archivo.red()
        print("Archivo leido correctamente.\n")
        analizar_codigo(codigo) # Analizar el código
        # Mostrar el código que se lee en la terminal
        print("\n----- Codigo leido desde el archivo -----\n")
        for i, linea in enumerate(contenido, start=1):
            print(f"{i}: {linea.strip()}")  # Imprimir con número de línea
        
        return contenido
    except FileNotFoundError:
        print("Error: No se encontro el archivo.")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

# Archivo donde está el código de ejemplo
ruta_archivo = "codigo_fuente.txt"
lineas = leer_archivo(ruta_archivo)