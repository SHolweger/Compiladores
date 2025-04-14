import ply.yacc as yacc
from lexer import tokens, lexer, errores_lexicos, tokens_extraidos
import html_gen
from html_gen import abrir_todos_los_html

# Tabla de símbolos y errores
tabla_simbolos = {}
errores_sintacticos = []

#TABLA DE SIMBOLOS
def agregar_simbolo(nombre, tipo, valor, linea):
    tipo = tipo.lower()
    if nombre in tabla_simbolos:
        errores_sintacticos.append((f"Error: La variable '{nombre}' ya ha sido declarada.", linea))
    else:
        tabla_simbolos[nombre] = {'tipo': tipo, 'valor': valor}

def actualizar_simbolo(nombre, valor, linea):
    if nombre in tabla_simbolos:
        tipo = tabla_simbolos[nombre]['tipo']
        if tipo == 'numero' and isinstance(valor, int):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'decimal' and isinstance(valor, float):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'booleano' and isinstance(valor, bool):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'cadena' and isinstance(valor, str):  
            tabla_simbolos[nombre]['valor'] = valor
        else:
            errores_sintacticos.append((f"Tipo de dato incorrecto para la variable '{nombre}'", linea))
    else:
        errores_sintacticos.append((f"La variable '{nombre}' no ha sido declarada.", linea))

def verificar_simbolo(nombre, linea):
    if nombre not in tabla_simbolos:
        errores_sintacticos.append((f"La variable '{nombre}' no ha sido declarada.", linea))
        return False
    return True

# Reglas de gramática
def p_programa(p):
    '''programa : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    print("Código válido: Estructura 'inicio() {}' reconocida.")

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias
                  | empty''' 
    pass

def p_empty(p):
    '''empty : '''  
    pass

def p_sentencia_declaracion(p):
    '''sentencia : NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | BOOLEANO IDENTIFICADOR IGUAL booleano PUNTOYCOMA
                 | CADENA IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    agregar_simbolo(p[2], p[1], p[4], p.lineno(2)) 

def p_sentencia_asignacion(p):
    '''sentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    if verificar_simbolo(p[1], p.lineno(1)):
        actualizar_simbolo(p[1], p[3], p.lineno(1))

def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                 | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_mientras(p):
    '''sentencia : MIENTRAS PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_regresa(p):
    '''sentencia : REGRESA valor PUNTOYCOMA'''
    if isinstance(p[2], str):
        print(f"Regresando valor: {p[2]}")

def p_expresion(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | NUMERO
                 | DECIMAL
                 | CADENA
                 | IDENTIFICADOR'''

    if len(p) == 2:
        if isinstance(p[1], str):  
            if p.slice[1].type == "IDENTIFICADOR":
                nombre = p[1]
                if verificar_simbolo(nombre, p.lineno(1)):
                    p[0] = tabla_simbolos[nombre]["valor"]
                else:
                    p[0] = 0  
            else:
                p[0] = p[1]  
        else:
            p[0] = p[1]  
    else:
        if isinstance(p[1], (int, float)) and isinstance(p[3], (int, float)):
            if p[2] == '+': p[0] = p[1] + p[3]
            elif p[2] == '-': p[0] = p[1] - p[3]
            elif p[2] == '*': p[0] = p[1] * p[3]
            elif p[2] == '/': p[0] = p[1] / p[3]
        else:
            errores_sintacticos.append(("Operacion no valida entre tipos diferentes.", p.lineno(2)))

def p_booleano(p):
    '''booleano : VERDADERO
                | FALSO'''
    p[0] = True if p[1] == 'verdadero' else False

def p_condicion(p):
    '''condicion : IDENTIFICADOR MAYOR valor
                 | IDENTIFICADOR MENOR valor
                 | IDENTIFICADOR IGUAL_IGUAL valor
                 | valor MAYOR IDENTIFICADOR
                 | valor MENOR IDENTIFICADOR
                 | valor IGUAL_IGUAL IDENTIFICADOR'''
    if isinstance(p[1], str) and p.slice[1].type == "IDENTIFICADOR":
        verificar_simbolo(p[1], p.lineno(1))
    if isinstance(p[3], str) and p.slice[3].type == "IDENTIFICADOR":
        verificar_simbolo(p[3], p.lineno(3))

def p_valor(p):
    '''valor : NUMERO
             | DECIMAL
             | CADENA
             | VERDADERO
             | FALSO
             | IDENTIFICADOR'''
    p[0] = p[1]

def p_error(p):
    if p:
        errores_sintacticos.append((f"Error de sintaxis en la linea {p.lineno}: Token inesperado '{p.value}'", p.lineno))
    else:
        errores_sintacticos.append(("Error de sintaxis: Fin de archivo inesperado", 0))

parser = yacc.yacc()

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print(" Archivo leído correctamente.\n")
        return contenido
    except FileNotFoundError:
        print(" Error: No se encontro el archivo.")
        return None

#PARSER
def analizar_sintaxis(archivo):
    data = leer_archivo(archivo)
    if data:
        lexer.lineno = 1
        print("\n🔍 Analizando sintaxis del código...\n")
        parser.parse(data, lexer=lexer)
        print("Analisis sintactico finalizado.\n")
        html_gen.generar_pagina_inicio()
        html_gen.generar_html_tokens(tokens_extraidos)
        html_gen.generar_html_errores(errores_lexicos + errores_sintacticos)
        html_gen.generar_html_tabla_simbolos(tabla_simbolos)

# Punto de entrada
if __name__ == "__main__":
    #analizar_sintaxis("codigo_fuente.txt")
    # ESTO ES PARA SEBAS EN MAC XD
    analizar_sintaxis("COMPILADOR Proyecto/codigo_fuente.txt")
 # type: ignore