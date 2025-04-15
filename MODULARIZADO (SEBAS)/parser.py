# parser.py

import ply.yacc as yacc
import lexer
from errores import registrar_error, errores_sintacticos, errores_semanticos, limpiar_errores
from tabla_simbolos import agregar_simbolo, actualizar_simbolo, obtener_simbolo
from semantico import evaluar_expresion, tipo_valido

tokens = lexer.tokens
encontrar_columna = lexer.encontrar_columna  # Alias para facilitar uso

# Precedencia de operadores
precedence = (
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIVIDIDO'),
    ('left', 'MAYOR', 'MENOR', 'IGUAL', 'DIFERENTE'),
    ('left', 'Y', 'O'),
    ('right', 'NO'),
)

# Reglas gramaticales

def p_programa(p):
    'programa : INICIO PARENTESIS_A PARENTESIS_C LLAVE_A instrucciones LLAVE_C'
    p[0] = ('programa', p[5])

def p_instrucciones(p):
    '''instrucciones : instrucciones instruccion
                     | instruccion'''
    p[0] = p[1] + [p[2]] if len(p) == 3 else [p[1]]

def p_instruccion_declaracion(p):
    'instruccion : tipo ID IGUAL expresion PUNTOYCOMA'
    tipo, nombre, valor = p[1], p[2], p[4]
    if tipo_valido(tipo, valor):
        agregar_simbolo(nombre, tipo, valor, p.lineno(2))
    else:
        registrar_error(errores_semanticos,
            f"Error de tipo: No se puede asignar '{valor}' al tipo '{tipo}'",
            p.lineno(2), find_column(p.lexer.lexdata, p.slice[2]))
    p[0] = ('declaracion', tipo, nombre, valor)

def p_instruccion_asignacion(p):
    'instruccion : ID IGUAL expresion PUNTOYCOMA'
    nombre, valor = p[1], p[3]
    simbolo = obtener_simbolo(nombre)
    if simbolo:
        tipo = simbolo['tipo']
        if tipo_valido(tipo, valor):
            actualizar_simbolo(nombre, valor)
        else:
            registrar_error(errores_semanticos,
                f"Error de tipo: No se puede asignar '{valor}' a la variable '{nombre}' de tipo '{tipo}'",
                p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
    else:
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{nombre}' no declarada.",
            p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
    p[0] = ('asignacion', nombre, valor)

def p_instruccion_si(p):
    'instruccion : SI PARENTESIS_A expresion PARENTESIS_C LLAVE_A instrucciones LLAVE_C SINO LLAVE_A instrucciones LLAVE_C'
    condicion = p[3]
    if isinstance(condicion, bool):
        p[0] = ('si', condicion, p[6], p[10])
    else:
        registrar_error(errores_semanticos,
            "Error de tipo: La condición en 'si' no es booleana.",
            p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
        p[0] = ('si', False, p[6], p[10])

def p_instruccion_mientras(p):
    'instruccion : MIENTRAS PARENTESIS_A expresion PARENTESIS_C LLAVE_A instrucciones LLAVE_C'
    condicion = p[3]
    if isinstance(condicion, bool):
        p[0] = ('mientras', condicion, p[6])
    else:
        registrar_error(errores_semanticos,
            "Error de tipo: La condición en 'mientras' no es booleana.",
            p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
        p[0] = ('mientras', False, p[6])

def p_instruccion_retorno(p):
    'instruccion : REGRESA expresion PUNTOYCOMA'
    p[0] = ('regresa', p[2])

def p_expresion_binaria(p):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion IGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion Y expresion
                 | expresion O expresion'''
    p[0] = evaluar_expresion(p[1], p[2], p[3], p.lineno(2))

def p_expresion_unaria(p):
    'expresion : NO expresion'
    if isinstance(p[2], bool):
        p[0] = not p[2]
    else:
        registrar_error(errores_semanticos,
            "Error de tipo: Operador 'NO' requiere una expresión booleana.",
            p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
        p[0] = False

def p_expresion_valor(p):
    '''expresion : NUMERO
                 | DECIMAL
                 | CADENA
                 | BOOLEANO'''
    p[0] = p[1]

def p_expresion_id(p):
    'expresion : ID'
    simbolo = obtener_simbolo(p[1])
    if simbolo:
        p[0] = simbolo['valor']
    else:
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{p[1]}' no declarada.",
            p.lineno(1), find_column(p.lexer.lexdata, p.slice[1]))
        p[0] = 0

def p_error(p):
    if p:
        registrar_error(errores_sintacticos,
            f"Error de sintaxis: Token inesperado '{p.value}'",
            p.lineno, find_column(p.lexer.lexdata, p))
    else:
        registrar_error(errores_sintacticos,
            "Error de sintaxis: Fin de archivo inesperado",
            0, 0)

# Función principal para analizar código
def analizar_sintaxis(codigo):
    parser = yacc.yacc()
    limpiar_errores()
    parser.parse(codigo, lexer=lexer)
    return errores_sintacticos + errores_semanticos
