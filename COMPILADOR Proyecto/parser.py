import ply.yacc as yacc
from lexer import tokens, lexer, errores_lexicos, tokens_extraidos,encontrar_columna
import html_gen
from html_gen import abrir_todos_los_html
from tkinter import Tk, filedialog

# Tabla de símbolos y errores
tabla_simbolos = {} # Almacena las variables y sus atributos
errores_sintacticos = [] # Lista de errores sintácticos
errores_semanticos = [] # Lista de errores semánticos
pila_ambitos = ["global"] # Pila de ámbitos para manejar el contexto de las variables

#AMBITOS VARIABLES
def entrar_ambito(nuevo_ambito):  # Cambiar el ámbito actual
    pila_ambitos.append(nuevo_ambito)

def salir_ambito():  # Salir del ámbito actual
    if len(pila_ambitos) > 1:  # Evitar eliminar el ámbito global
        pila_ambitos.pop()

def obtener_ambito_actual(): # Obtener el ámbito actual
    return pila_ambitos[-1]

# Tabla de símbolos
def agregar_simbolo(nombre, tipo, valor, linea, columna, modificable=True):  # Agregar una nueva variable a la tabla de símbolos
    tipo = tipo.lower()
    ambito = obtener_ambito_actual()
    if nombre in tabla_simbolos and tabla_simbolos[nombre]['ambito'] == ambito:
        errores_sintacticos.append((f"Error Sintáctico: La variable '{nombre}' ya ha sido declarada en el ámbito '{ambito}'.", linea, columna))
    else:
        tabla_simbolos[nombre] = {
            'tipo': tipo,
            'ambito': ambito,
            'valor': valor,
            'linea': linea,
            'columna': columna,
            'referencia': ambito if ambito != "global" else "global", # Referencia al ámbito de la variable
            'modificable': modificable,
            'usado': False  # Inicialmente no utilizada
        }

def actualizar_simbolo(nombre, valor, linea, columna):  # Actualizar el valor de una variable existente
    if nombre in tabla_simbolos:
        simbolo = tabla_simbolos[nombre]
        if not simbolo['modificable']:
            errores_semanticos.append((f"Error semántico: La variable '{nombre}' es constante y no puede ser modificada.", linea, columna))
            return

        tipo = simbolo['tipo']
        if tipo == 'numero' and isinstance(valor, int):
            simbolo['valor'] = valor
        elif tipo == 'decimal' and isinstance(valor, float):
            simbolo['valor'] = valor
        elif tipo == 'booleano' and isinstance(valor, bool):
            simbolo['valor'] = valor
        elif tipo == 'cadena' and isinstance(valor, str):
            simbolo['valor'] = valor
        else:
            errores_sintacticos.append((f"Error Sintáctico: Tipo incorrecto para la variable '{nombre}'.", linea, columna))
    else:
        errores_semanticos.append((f"Error Semántico: La variable '{nombre}' no ha sido declarada.", linea, columna))

def verificar_simbolo(nombre, linea, columna):  # Verificar si una variable existe en la tabla de símbolos
    ambito = obtener_ambito_actual()
    for amb in [ambito, "global"]:
        if nombre in tabla_simbolos and tabla_simbolos[nombre]['ambito'] == amb:
            tabla_simbolos[nombre]['usado'] = True  # Marcar como utilizada
            return True
    errores_semanticos.append((f"Error Semántico: La variable '{nombre}' no ha sido declarada en el ámbito '{ambito}'.", linea, columna))
    return False

# Reglas de gramática
def p_programa(p):  # Regla de inicio del programa
    '''programa : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    print("Código válido: Estructura 'inicio() {}' reconocida.")

def p_sentencias(p):  # Regla de sentencias
    '''sentencias : sentencia
                  | sentencia sentencias
                  | empty''' 
    pass

def p_empty(p):     # Regla para manejar la producción vacía
    '''empty : '''  
    pass

def p_sentencia_declaracion(p):
    '''sentencia : NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | BOOLEANO IDENTIFICADOR IGUAL booleano PUNTOYCOMA
                 | CADENA IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    # Mapeo de tipos esperados
    tipo_python = {'numero': int, 'decimal': float, 'booleano': bool, 'cadena': str}

    # Validar si el tipo de la expresión coincide con el tipo declarado
    if not isinstance(p[4], tipo_python[p[1].lower()]):
        errores_semanticos.append((f"Error semántico: La variable '{p[2]}' de tipo '{p[1]}' no puede recibir un valor de tipo '{type(p[4]).__name__}'.", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
        return  # Detener el procesamiento

    # Si los tipos coinciden, agregar el símbolo
    agregar_simbolo(p[2], p[1], p[4], p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2]))
    p[0] = p[4]  # Asignar el valor de la expresión a p[0]

def p_sentencia_asignacion(p):  # Regla para asignación de valores a variables
    '''sentencia : IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    # Verificar si la variable está declarada
    columna = encontrar_columna(lexer.lexdata, p.slice[1])
    if verificar_simbolo(p[1], p.lineno(1), columna):
        # Validar si la expresión es None
        if p[3] is None:
            errores_semanticos.append((f"Error semántico: No se puede asignar un valor nulo a la variable '{p[1]}'.", p.lineno(1), columna))
            return

        # Obtener el tipo de la variable y el tipo del valor
        tipo_variable = tabla_simbolos[p[1]]['tipo']
        tipo_valor = type(p[3]).__name__

        # Mapeo de tipos esperados
        tipo_python = {'numero': int, 'decimal': float, 'booleano': bool, 'cadena': str}

        # Validar si el tipo del valor coincide con el tipo de la variable
        if not isinstance(p[3], tipo_python.get(tipo_variable)):
            errores_semanticos.append((f"Error semántico: Asignación no válida. Variable '{p[1]}' de tipo '{tipo_variable}' no puede recibir un valor de tipo '{tipo_valor}'.", p.lineno(1), columna))
            return

        # Si los tipos coinciden, actualizar el valor de la variable
        actualizar_simbolo(p[1], p[3], p.lineno(1), columna)
    else:
        # Si la variable no está declarada, registrar un error
        errores_semanticos.append((f"Error semántico: La variable '{p[1]}' no ha sido declarada.", p.lineno(1), columna))
    
def p_sentencia_si(p):  # Regla para sentencia 'si'
    '''sentencia : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                 | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    entrar_ambito("local_si")  # Cambiar a un ámbito local específico
    # Verificar las variables usadas en la condición
    if isinstance(p[3], str) and p.slice[3].type == "IDENTIFICADOR":
        if not verificar_simbolo(p[3], p.lineno(3), encontrar_columna(lexer.lexdata, p.slice[3])):
            return  # Detener el procesamiento si hay un error
        
    salir_ambito()  # Salir del ámbito al finalizar el bloque
    if len(p) == 12:  # Si hay un bloque `sino`
        entrar_ambito("local_sino")  # Cambiar a un ámbito local específico
    if isinstance(p[3], str) and p.slice[3].type == "IDENTIFICADOR":
        if not verificar_simbolo(p[3], p.lineno(3), encontrar_columna(lexer.lexdata, p.slice[3])):
            return  # Detener el procesamiento si hay un error
        salir_ambito()

def p_sentencia_mientras(p):  # Regla para sentencia 'mientras'
    '''sentencia : MIENTRAS PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER'''
    entrar_ambito("local_mientras")  # Cambiar a un ámbito local específico
    # Verificar las variables usadas en la condición
    if isinstance(p[3], str) and p.slice[3].type == "IDENTIFICADOR":
        if not verificar_simbolo(p[3], p.lineno(3), encontrar_columna(lexer.lexdata, p.slice[3])):
            return  # Detener el procesamiento si hay un error
    salir_ambito()  # Salir del ámbito al finalizar el bloque

def p_sentencia_regresa(p):  # Regla para sentencia 'regresa'
    '''sentencia : REGRESA valor PUNTOYCOMA'''
    # Mapeo de tipos permitidos
    tipos_permitidos = (int, float, str, bool)

    if not isinstance(p[2], tipos_permitidos):
        errores_semanticos.append((f"Error semántico: El valor retornado '{p[2]}' no es de un tipo permitido.", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
        return

    print(f"Regresando valor: {p[2]}")

def p_expresion(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | PARENIZQ expresion PARENDER
                 | NUMERO
                 | DECIMAL
                 | CADENA
                 | IDENTIFICADOR'''

    if len(p) == 2:  # Caso base: un solo valor
        if isinstance(p[1], str) and p.slice[1].type == "IDENTIFICADOR":
            nombre = p[1]
            if verificar_simbolo(nombre, p.lineno(1), encontrar_columna(lexer.lexdata, p.slice[1])):
                p[0] = tabla_simbolos[nombre]["valor"]
            else:
                errores_semanticos.append((f"Error semántico: La variable '{nombre}' no ha sido declarada.", p.lineno(1), encontrar_columna(lexer.lexdata, p.slice[1])))
                p[0] = None  # Detener el procesamiento
        else:
            p[0] = p[1]
    else:  # Operaciones aritméticas
        # Resolver valores si son identificadores
        for i in [1, 3]:  # Validar ambos operandos
            if isinstance(p[i], str) and p.slice[i].type == "IDENTIFICADOR":
                if verificar_simbolo(p[i], p.lineno(i), encontrar_columna(lexer.lexdata, p.slice[i])):
                    p[i] = tabla_simbolos[p[i]]["valor"]
                else:
                    errores_semanticos.append((f"Error semántico: La variable '{p[i]}' no ha sido declarada.", p.lineno(i), encontrar_columna(lexer.lexdata, p.slice[i])))
                    p[0] = None
                    return  # Detener el procesamiento

        # Validar si alguno de los operandos es None
        if p[1] is None or p[3] is None:
            errores_semanticos.append((f"Error semántico: Operación no válida debido a un valor nulo.", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
            p[0] = None
            return

        # Validar tipos antes de realizar la operación
        if isinstance(p[1], (int, float)) and isinstance(p[3], (int, float)):  # Operaciones entre números
            if p[2] == '+': p[0] = p[1] + p[3]
            elif p[2] == '-': p[0] = p[1] - p[3]
            elif p[2] == '*': p[0] = p[1] * p[3]
            elif p[2] == '/':
                if p[3] != 0:
                    p[0] = p[1] / p[3]
                else:
                    errores_semanticos.append((f"Error semántico: División entre cero.", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
                    p[0] = None
        elif isinstance(p[1], str) and isinstance(p[3], str):  # Concatenación de cadenas
            if p[2] == '+':  # Concatenación
                p[0] = p[1] + p[3]
            else:  # Operadores no válidos para cadenas
                errores_semanticos.append((f"Error semántico: Operación '{p[2]}' no válida entre cadenas.", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
                p[0] = None
        else:
            errores_semanticos.append((f"Error semántico: Operación no válida entre tipos '{type(p[1]).__name__}' y '{type(p[3]).__name__}'", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))
            p[0] = None  # Detener el procesamiento
        
def p_booleano(p):  # Regla para evaluar valores booleanos
    '''booleano : VERDADERO
                | FALSO'''
    p[0] = True if p[1] == 'verdadero' else False

def p_condicion(p):  # Regla para comparaciones de valores
    '''condicion : IDENTIFICADOR MAYOR valor
                 | IDENTIFICADOR MENOR valor
                 | IDENTIFICADOR IGUAL_IGUAL valor
                 | IDENTIFICADOR DIFERENTE valor
                 | valor MAYOR IDENTIFICADOR
                 | valor MENOR IDENTIFICADOR
                 | valor IGUAL_IGUAL IDENTIFICADOR
                 | valor DIFERENTE IDENTIFICADOR'''

# Validar tipos antes de realizar la comparación
    if type(p[1]) != type(p[3]):
        errores_semanticos.append((f"Error semantico: Comparacion no valida entre tipos '{type(p[1]).__name__}' y '{type(p[3]).__name__}'", p.lineno(2), encontrar_columna(lexer.lexdata, p.slice[2])))

    # Verificar si los operandos son identificadores y obtener sus valores
    if isinstance(p[1], str) and p.slice[1].type == "IDENTIFICADOR":
        if verificar_simbolo(p[1], p.lineno(1), encontrar_columna(lexer.lexdata, p.slice[1])):
            p[1] = tabla_simbolos[p[1]]["valor"]
    if isinstance(p[3], str) and p.slice[3].type == "IDENTIFICADOR":
        if verificar_simbolo(p[3], p.lineno(3), encontrar_columna(lexer.lexdata, p.slice[3])):
            p[3] = tabla_simbolos[p[3]]["valor"]
        
def p_valor(p):  # Regla para evaluar valores
    '''valor : NUMERO
             | DECIMAL
             | CADENA
             | IDENTIFICADOR'''
    if p.slice[1].type == "IDENTIFICADOR":
        nombre = p[1]
        if verificar_simbolo(nombre, p.lineno(1), encontrar_columna(lexer.lexdata, p.slice[1])):
            p[0] = tabla_simbolos[nombre]["valor"]
        else:
            p[0] = None
    else:
        p[0] = p[1]

def p_sentencia_funcion(p):
    '''sentencia : IDENTIFICADOR PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    entrar_ambito(f"funcion_{p[1]}")
    p[0] = p[5]  # procesar sentencias dentro del nuevo ámbito
    salir_ambito()

def p_error(p):  # Regla para manejar errores sintácticos
    if p:
        # Calcular la columna correctamente
        col = encontrar_columna(lexer.lexdata, p)
        errores_sintacticos.append((f"Error de sintaxis: Token inesperado '{p.value}'", p.lineno, col))
    else:
        errores_sintacticos.append(("Error de sintaxis: Fin de archivo inesperado", 0, -1))

parser = yacc.yacc()

def leer_archivo(ruta): # Leer el archivo de código fuente
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print(" Archivo leído correctamente.\n")
        return contenido
    except FileNotFoundError:
        print(" Error: No se encontro el archivo.")
        return None

def detectar_variables_no_utilizadas(): # Detectar variables no utilizadas
    for nombre, datos in tabla_simbolos.items():
        if not datos['usado']:
            errores_semanticos.append((f"Advertencia: La variable '{nombre}' fue declarada pero no utilizada.", datos['linea'], datos['columna']))

#PARSER
def analizar_sintaxis(archivo): # Analizar la sintaxis del código fuente
    data = leer_archivo(archivo)
    if data:
        lexer.lineno = 1
        print("\n Analizando sintaxis del codigo...\n")
        parser.parse(data, lexer=lexer)
        print("Analisis sintactico finalizado.\n")        
        detectar_variables_no_utilizadas()  # Detectar variables no utilizadas
        html_gen.generar_pagina_inicio()
        html_gen.generar_html_tokens(tokens_extraidos)
        html_gen.generar_html_errores(errores_lexicos + errores_sintacticos+errores_semanticos)
        html_gen.generar_html_tabla_simbolos(tabla_simbolos)

#
def seleccionar_archivo(): # Función para seleccionar un archivo de código fuente
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    return archivo

# Reemplazar la ruta fija por la función de selección
ruta_archivo = seleccionar_archivo()
if ruta_archivo:
    leer_archivo(ruta_archivo)
else:
    print("No se selecciono ningun archivo.")
#

# Punto de entrada
if __name__ == "__main__": 
    analizar_sintaxis(ruta_archivo)
    #analizar_sintaxis("COMPILADOR Proyecto/codigo_fuente.txt")
    # ESTO ES PARA SEBAS EN MAC XD
    # analizar_sintaxis("COMPILADOR Proyecto/codigo_fuente.txt")
 # type: ignore
 
 