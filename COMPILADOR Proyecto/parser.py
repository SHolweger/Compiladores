import ply.yacc as yacc
from lexer import tokens, lexer 

# Tabla de simbolos
tabla_simbolos = {}

def agregar_simbolo(nombre, tipo, valor):
    if nombre in tabla_simbolos:
        print(f"Error: La variable '{nombre}' ya ha sido declarada.")
    else:
        tabla_simbolos[nombre] = {'tipo': tipo, 'valor': valor}

def verificar_simbolo(nombre):
    if nombre not in tabla_simbolos:
        print(f"Error: La variable '{nombre}' no ha sido declarada.")
        return False
    return True

def p_programa(p):
    '''programa : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    print("Codigo valido: Estructura 'inicio() {}' reconocida.")

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    pass

def p_sentencia_declaracion(p):
    '''sentencia : NUMERO IDENTIFICADOR IGUAL NUMERO PUNTOYCOMA
                 | DECIMAL IDENTIFICADOR IGUAL DECIMAL PUNTOYCOMA'''
    agregar_simbolo(p[2], p[1], p[4])

def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                 | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_regresa(p):
    '''sentencia : REGRESA IDENTIFICADOR PUNTOYCOMA'''
    if verificar_simbolo(p[2]):
        print(f"Regresando valor de '{p[2]}': {tabla_simbolos[p[2]]['valor']}")

def p_condicion(p):
    '''condicion : IDENTIFICADOR MAYOR IDENTIFICADOR
                 | IDENTIFICADOR MENOR IDENTIFICADOR
                 | IDENTIFICADOR IGUAL_IGUAL IDENTIFICADOR'''
    if verificar_simbolo(p[1]) and verificar_simbolo(p[3]):
        pass

def p_error(p):
    if p:
        print(f"Error de sintaxis en la linea {p.lineno}: Token inesperado '{p.value}'")
    else:
        print("Error de sintaxis: Fin de archivo inesperado")

parser = yacc.yacc()

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print("Archivo leido correctamente.\n")
        return contenido
    except FileNotFoundError:
        print("Error: No se encontro el archivo.")
        return None

def analizar_sintaxis(archivo):
    data = leer_archivo(archivo)
    if data:
        print("\nAnalizando sintaxis del codigo...\n")
        result = parser.parse(data, lexer=lexer)
        print("Analisis sintactico finalizado.")

if __name__ == "__main__":
    analizar_sintaxis("codigo_fuente.txt")
