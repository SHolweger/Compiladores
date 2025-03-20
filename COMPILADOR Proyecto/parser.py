import ply.yacc as yacc
from lexer import tokens, lexer 

def p_programa(p):
    '''programa : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    print("✅ Código válido: Estructura 'inicio() {}' reconocida.")

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    pass

def p_sentencia_declaracion(p):
    '''sentencia : NUMERO IDENTIFICADOR IGUAL NUMERO PUNTOYCOMA
                 | DECIMAL IDENTIFICADOR IGUAL DECIMAL PUNTOYCOMA'''
    pass

def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                 | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_regresa(p):
    '''sentencia : REGRESA IDENTIFICADOR PUNTOYCOMA'''
    pass    

def p_condicion(p):
    '''condicion : IDENTIFICADOR MAYOR IDENTIFICADOR
                 | IDENTIFICADOR MENOR IDENTIFICADOR
                 | IDENTIFICADOR IGUAL_IGUAL IDENTIFICADOR'''
    pass

# ERRORES SINTACTICOS
def p_error(p):
    if p:
        print(f"❌ Error de sintaxis en la línea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("❌ Error de sintaxis: Fin de archivo inesperado")

# PARSER
parser = yacc.yacc()

# LEER ARCHIVOS
def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print("✅ Archivo leído correctamente.\n")
        return contenido
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo.")
        return None

def analizar_sintaxis(archivo):
    data = leer_archivo(archivo)
    if data:
        print("\n📌 Analizando sintaxis del código...\n")
        result = parser.parse(data, lexer=lexer)  # 📌 Pasamos el lexer al parser
        print("✅ Análisis sintáctico finalizado.")

# TXT PRUEBA
if __name__ == "__main__":
    analizar_sintaxis("codigo_fuente.txt")
