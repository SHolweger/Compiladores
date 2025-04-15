# Parser.py
import ply.yacc as yacc
from lexer import lexer, tokens
from tabla_simbolos import tabla_simbolos, errores_sintacticos, errores_semanticos, agregar_simbolo, actualizar_simbolo, verificar_simbolo

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
    tipo = p[1]
    nombre = p[2]
    valor = p[4]
    linea = p.lineno(2)
    
    # Verificar si la variable ya está declarada
    if nombre in tabla_simbolos:
        errores_semanticos.append((f"Error semántico en línea {linea}: La variable '{nombre}' ya fue declarada.", linea))
    else:
        agregar_simbolo(nombre, tipo, valor, linea)

# Sentencia de asignación
def p_sentencia_asignacion(p):
    '''sentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    nombre = p[1]
    valor = p[3]
    linea = p.lineno(1)

    if verificar_simbolo(nombre, linea):
        tipo = tabla_simbolos[nombre]["tipo"]
        if not tipo_valido(tipo, valor):
            errores_semanticos.append((f"Error semántico en línea {linea}: No se puede asignar un valor de tipo {type(valor).__name__} a la variable '{nombre}' de tipo {tipo}.", linea))
        else:
            actualizar_simbolo(nombre, valor, linea)
    else:
        errores_semanticos.append((f"Error semántico en línea {linea}: La variable '{nombre}' no está declarada.", linea))

def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                 | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_mientras(p):
    '''sentencia : MIENTRAS PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER'''
    pass

def p_sentencia_regresa(p):
    '''sentencia : REGRESA valor PUNTOYCOMA'''
    print(f"Regresando valor: {p[2]}")

def p_expresion(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion AND expresion
                 | expresion OR expresion
                 | NOT expresion
                 | NUMERO
                 | DECIMAL
                 | CADENA
                 | IDENTIFICADOR'''

    if len(p) == 2:
        # Caso de un solo operando (numero, decimal, cadena o identificador)
        if p.slice[1].type == "IDENTIFICADOR":
            nombre = p[1]
            if verificar_simbolo(nombre, p.lineno(1)):
                p[0] = tabla_simbolos[nombre]["valor"]
            else:
                errores_semanticos.append((f"Error semantico en linea {p.lineno(1)}: Variable '{nombre}' no declarada.", p.lineno(1)))
                p[0] = 0
        else:
            p[0] = p[1]

    else:
        op1 = p[1]
        op2 = p[3]
        operador = p[2]
        linea = p.lineno(2)

        # Operaciones matematicas entre números
        if isinstance(op1, (int, float)) and isinstance(op2, (int, float)):
            if operador == '+':
                p[0] = op1 + op2
            elif operador == '-':
                p[0] = op1 - op2
            elif operador == '*':
                p[0] = op1 * op2
            elif operador == '/':
                if op2 == 0:
                    errores_semanticos.append((f"Error semantico en linea {linea}: Division por cero.", linea))
                    p[0] = 0
                else:
                    p[0] = op1 / op2

        # Operaciones booleanas
        elif isinstance(op1, bool) and isinstance(op2, bool):
            if operador == 'AND':
                p[0] = op1 and op2
            elif operador == 'OR':
                p[0] = op1 or op2

        # Operación NOT unaria
        elif operador == 'NOT':
            if isinstance(op1, bool):
                p[0] = not op1
            else:
                errores_semanticos.append((f"Error semantico en linea {linea}: El operador 'NOT' solo es válido para valores booleanos.", linea))
                p[0] = False

        # Comparaciones booleanas con otros tipos
        elif isinstance(op1, bool) or isinstance(op2, bool):
            errores_semanticos.append((f"Error semantico en linea {linea}: Operación no válida entre tipos {type(op1).__name__} y {type(op2).__name__}.", linea))
            p[0] = False

        # Manejo de errores para operaciones entre tipos incompatibles
        else:
            errores_semanticos.append((f"Error semantico en linea {linea}: Operación no válida entre tipos {type(op1).__name__} y {type(op2).__name__}.", linea))
            p[0] = 0

def p_booleano(p):
    '''booleano : VERDADERO
                | FALSO'''
    p[0] = True if p[1] == 'verdadero' else False

def p_condicion(p): 
    '''condicion : IDENTIFICADOR MAYOR valor
                 | IDENTIFICADOR MENOR valor
                 | IDENTIFICADOR IGUAL_IGUAL valor
                 | IDENTIFICADOR MAYOR_IGUAL valor
                 | IDENTIFICADOR MENOR_IGUAL valor
                 | IDENTIFICADOR DIFERENTE valor
                 | valor MAYOR IDENTIFICADOR
                 | valor MENOR IDENTIFICADOR
                 | valor IGUAL_IGUAL IDENTIFICADOR
                 | valor MAYOR_IGUAL IDENTIFICADOR
                 | valor MENOR_IGUAL IDENTIFICADOR
                 | valor DIFERENTE IDENTIFICADOR
                 | condicion AND condicion
                 | condicion OR condicion
                 | NOT condicion
                 | PARENIZQ condicion PARENDER'''
    
    linea = p.lineno(1)  # Tomamos la línea de la primera parte de la expresión
    op1 = p[1]           # El primer operando
    op2 = p[3]           # El segundo operando (si es aplicable)
    operador = p[2]      # El operador de la condición

    if len(p) == 2:  # Caso de NOT o paréntesis
        if p[1] == 'NOT':  # Negación
            p[0] = not p[2]
        elif p[1] == 'PARENIZQ':  # Paréntesis
            p[0] = p[2]

    elif len(p) == 3:  # Caso de comparación entre dos expresiones
        # Si op1 es un identificador, obtenemos su valor
        if isinstance(op1, str) and p.slice[1].type == "IDENTIFICADOR":
            if verificar_simbolo(op1, p.lineno(1)):
                op1 = tabla_simbolos[op1]["valor"]
            else:
                op1 = 0  # Si no está declarado, le asignamos un valor predeterminado
        
        # Si op2 es un identificador, obtenemos su valor
        if isinstance(op2, str) and p.slice[3].type == "IDENTIFICADOR":
            if verificar_simbolo(op2, p.lineno(3)):
                op2 = tabla_simbolos[op2]["valor"]
            else:
                op2 = 0  # Si no está declarado, le asignamos un valor predeterminado

        # Validación de tipos para comparaciones
        if type(op1) != type(op2):
            errores_semanticos.append((f"Error semántico en línea {linea}: Comparación entre tipos incompatibles: {type(op1).__name__} y {type(op2).__name__}.", linea))
            p[0] = False
            return

        # Realizamos la comparación según el operador
        if operador == '>':
            p[0] = op1 > op2
        elif operador == '<':
            p[0] = op1 < op2
        elif operador == '==':
            p[0] = op1 == op2
        elif operador == '>=':
            p[0] = op1 >= op2
        elif operador == '<=':
            p[0] = op1 <= op2
        elif operador == '!=':
            p[0] = op1 != op2

    elif len(p) == 4:  # Caso de expresión lógica (AND/OR)
        if p[2] == 'AND':
            p[0] = p[1] and p[3]
        elif p[2] == 'OR':
            p[0] = p[1] or p[3]
        elif p[2] == 'NOT':
            p[0] = not p[3]

def p_error(p):
    if p:
        errores_sintacticos.append((f"Error sintáctico en línea {p.lineno}: {p.value}", p.lineno))
    else:
        errores_sintacticos.append(("Error sintáctico en fin de archivo", 0))

def tipo_valido(tipo, valor):
    if tipo == "numero" and isinstance(valor, (int, float)):
        return True
    elif tipo == "decimal" and isinstance(valor, float):
        return True
    elif tipo == "booleano" and isinstance(valor, bool):
        return True
    elif tipo == "cadena" and isinstance(valor, str):
        return True
    return False

# Función principal
def analizar_sintaxis(input_data):
    # Inicializar el parser
    parser = yacc.yacc()
    
    # Aquí no se necesita modificar lexer.lineno directamente
    resultado = parser.parse(input_data)
    return resultado

