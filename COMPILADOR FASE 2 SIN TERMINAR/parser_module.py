import ply.yacc as yacc
from lexer_module import tokens, lexer, encontrar_columna, analizar_codigo,encontrar_linea
import html_gen

# Precedencia de operadores
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV'),
    ('right', 'NEGACION'),
)

# Tabla de símbolos y errores
tabla_simbolos = {}
errores_sintacticos = []
errores_semanticos = []
pila_ambitos = ["global"]

# ===== ÁMBITOS =====
def entrar_ambito(nuevo_ambito):
    pila_ambitos.append(nuevo_ambito)

def salir_ambito():
    if len(pila_ambitos) > 1:
        pila_ambitos.pop()

def obtener_ambito_actual():
    return pila_ambitos[-1]

# ===== TABLA DE SÍMBOLOS CON ÁMBITOS =====
def buscar_simbolo(nombre):
    for ambito in reversed(pila_ambitos):
        clave = f"{nombre}_{ambito}"
        if clave in tabla_simbolos:
            return tabla_simbolos[clave]
    return None

def verificar_simbolo(nombre, linea, columna):
    simbolo = buscar_simbolo(nombre)
    if simbolo:
        simbolo['usado'] = True
        return True
    errores_semanticos.append((
        f"Error Semántico: La variable '{nombre}' no ha sido declarada en el ámbito actual.", 
        linea, columna
    ))
    return False

def actualizar_simbolo(nombre, valor, linea, columna):
    for ambito in reversed(pila_ambitos):
        clave = f"{nombre}_{ambito}"
        if clave in tabla_simbolos:
            simbolo = tabla_simbolos[clave]
            if not simbolo['modificable']:
                errores_semanticos.append((
                    f"Error semántico: La variable '{nombre}' es constante y no puede ser modificada.", 
                    linea, columna
                ))
                return
            tipo = simbolo['tipo']
            tipo_python = {'numero': int, 'decimal': float, 'booleano': bool, 'cadena': str}
            if not isinstance(valor, tipo_python.get(tipo)):
                errores_semanticos.append((
                    f"Error semántico: Tipo incorrecto para la variable '{nombre}'.", 
                    linea, columna
                ))
                return
            simbolo['valor'] = valor
            return
    errores_semanticos.append((
        f"Error Semántico: La variable '{nombre}' no ha sido declarada.", 
        linea, columna
    ))

def agregar_simbolo(nombre, tipo, valor, linea, columna, modificable=True, parametros=None, retorno=None):
    tipo = tipo.lower()
    ambito = obtener_ambito_actual()
    clave = f"{nombre}_{ambito}"

    if clave in tabla_simbolos:
        errores_sintacticos.append((
            f"Error Sintáctico: La variable '{nombre}' ya ha sido declarada en el ámbito '{ambito}'.",
            linea, columna
        ))
    else:
        tabla_simbolos[clave] = {
            'tipo': tipo,
            'ambito': ambito,
            'valor': valor,
            'linea': linea,
            'columna': columna,
            'referencia': ambito if ambito != "global" else "global",
            'modificable': modificable,
            'usado': False,
            'parametros': parametros,
            'retorno': retorno
        }

# ===== GRAMÁTICA Y SEMÁNTICA =====

def p_programa(p):
    '''programa : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    print("Código válido: Estructura 'inicio() {}' reconocida.")

def p_empty(p): 
    '''empty :'''
    pass

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]


def p_sentencia(p):
    '''sentencia : sentencia_funcion_declaracion
                 | sentencia_si
                 | sentencia_mientras
                 | sentencia_regresa
                 | sentencia_repetir
                 | sentencia_switch
                 | sentencia_llamada_funcion
                 | expresion
                 | sentencia_declaracion
                 | sentencia_asignacion'''
    pass

def p_sentencia_declaracion(p):
    '''sentencia_declaracion : NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                             | DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                             | BOOLEANO IDENTIFICADOR IGUAL booleano PUNTOYCOMA
                             | CADENA IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    
    tipo_python = {'numero': int, 'decimal': float, 'booleano': bool, 'cadena': str}
    tipo_decl = p[1].lower()
    valor = p[4]

    linea = encontrar_linea(lexer.lexdata, p.slice[2])  # ✅ Línea real
    columna = encontrar_columna(lexer.lexdata, p.slice[2])  # ✅ Columna real

    if not isinstance(valor, tipo_python[tipo_decl]):
        errores_semanticos.append((
            f"Error semántico: La variable '{p[2]}' de tipo '{p[1]}' no puede recibir un valor de tipo '{type(valor).__name__}'.",
            linea, columna
        ))
        return

    agregar_simbolo(p[2], p[1], valor, linea, columna)
    p[0] = valor


def p_sentencia_asignacion(p):
    '''sentencia_asignacion : IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    nombre = p[1]
    valor = p[3]
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    columna = encontrar_columna(lexer.lexdata, p.slice[1])
    if verificar_simbolo(nombre, linea, columna):
        if valor is None:
            errores_semanticos.append((f"Error semántico: No se puede asignar un valor nulo a la variable '{nombre}'.", linea, columna))
            return
        actualizar_simbolo(nombre, valor, linea, columna)

def p_sentencia_si(p):
    '''sentencia_si : SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER
                    | SI PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER SINO LLAVEIZQ sentencias LLAVEDER'''
    if not isinstance(p[3], bool):
        errores_semanticos.append((f"Error semántico: La condición en 'si' debe ser de tipo booleano.", encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1])))

def p_sentencia_mientras(p):
    '''sentencia_mientras : MIENTRAS PARENIZQ condicion PARENDER LLAVEIZQ sentencias LLAVEDER'''
    if not isinstance(p[3], bool):
        errores_semanticos.append((f"Error semántico: La condición en 'mientras' debe ser booleana.", encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1])))

def p_sentencia_regresa(p):
    '''sentencia_regresa : REGRESA expresion PUNTOYCOMA'''
    p[0] = p[2]  # Ya no hace falta verificar aquí, porque se hace en p_expresion

def p_sentencia_repetir(p):
    '''sentencia_repetir : REPETIR LLAVEIZQ sentencias LLAVEDER MIENTRAS PARENIZQ condicion PARENDER PUNTOYCOMA'''
    if not isinstance(p[7], bool):
        errores_semanticos.append((f"Error semántico: La condición en 'repetir mientras' debe ser booleana.", encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1])))

def p_sentencia_llamada_funcion(p):
    '''sentencia_llamada_funcion : IDENTIFICADOR PARENIZQ argumentos PARENDER PUNTOYCOMA'''
    nombre = p[1]
    args = p[3]
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    columna = encontrar_columna(lexer.lexdata, p.slice[1])

    simbolo = buscar_simbolo(nombre)
    if not simbolo or simbolo['tipo'] != 'funcion':
        errores_semanticos.append((f"Error semántico: La función '{nombre}' no está declarada.", linea, columna))
        return

    parametros = simbolo['parametros'] or []
    if len(args) != len(parametros):
        errores_semanticos.append((f"Error semántico: La función '{nombre}' esperaba {len(parametros)} argumentos pero se recibieron {len(args)}.", linea, columna))
        return

    tipo_python = {'numero': int, 'decimal': float, 'booleano': bool, 'cadena': str}
    for i, (arg, param) in enumerate(zip(args, parametros)):
        if not isinstance(arg, tipo_python.get(param['tipo'])):
            errores_semanticos.append((f"Error semántico: El argumento {i+1} de la función '{nombre}' debe ser de tipo '{param['tipo']}'.", linea, columna))
            return

def p_sentencia_switch(p):
    '''sentencia_switch : CAMBIAR PARENIZQ expresion PARENDER LLAVEIZQ casos LLAVEDER'''
    pass

def p_casos(p):
    '''casos : caso
             | caso casos'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

def p_caso(p):
    '''caso : CASO valor DOSPUNTOS sentencias
            | PREDETERMINADO DOSPUNTOS sentencias'''
    
    if p.slice[1].type == 'CASO':
        valor = p[2]
        ambito = f"caso_{valor}"
        sentencias = p[4]
    else:
        ambito = "predeterminado"
        sentencias = p[3]

    p[0] = ejecutar_bloque_con_ambito(sentencias, ambito)


def p_bloque_caso(p):
    '''bloque_caso : sentencias'''
    p[0] = p[1]

def ejecutar_bloque_con_ambito(sentencias, ambito):
    entrar_ambito(ambito)
    resultado = sentencias  # Aquí podrías ejecutar más lógica si lo necesitas
    salir_ambito()
    return resultado

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
    
    if len(p) == 2:
        if p.slice[1].type == "IDENTIFICADOR":
            simbolo = buscar_simbolo(p[1])
            if simbolo:
                verificar_simbolo(p[1], encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1]))  # <-- ✅ Marcar como usado aquí
                p[0] = simbolo["valor"]
            else:
                errores_semanticos.append((f"Error semántico: La variable '{p[1]}' no ha sido declarada.", encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1])))
                p[0] = None
        else:
            p[0] = p[1]
    else:
        for i in [1, 3]:
            if isinstance(p[i], str) and p.slice[i].type == "IDENTIFICADOR":
                simbolo = buscar_simbolo(p[i])
                if simbolo:
                    verificar_simbolo(p[i], p.lineno(i), encontrar_columna(lexer.lexdata, p.slice[i]))  # <-- ✅ También aquí
                    p[i] = simbolo["valor"]
                else:
                    errores_semanticos.append((f"Error semántico: La variable '{p[i]}' no ha sido declarada.", encontrar_linea(lexer.lexdata, p.slice[i]), encontrar_columna(lexer.lexdata, p.slice[i])))
                    p[0] = None
                    return
        if p[1] is None or p[3] is None:
            errores_semanticos.append((f"Error semántico: Operación no válida debido a un valor nulo.", encontrar_linea(lexer.lexdata, p.slice[2]), encontrar_columna(lexer.lexdata, p.slice[2])))
            p[0] = None
            return
        try:
            if p[2] == '+': p[0] = p[1] + p[3]
            elif p[2] == '-': p[0] = p[1] - p[3]
            elif p[2] == '*': p[0] = p[1] * p[3]
            elif p[2] == '/': p[0] = p[1] / p[3]
        except Exception:
            p[0] = None


def p_booleano(p):
    '''booleano : VERDADERO
                | FALSO'''
    p[0] = True if p[1] == 'verdadero' else False

def p_comparador(p):
    '''comparador : MENOR
                  | MAYOR
                  | MENOR_IGUAL
                  | MAYOR_IGUAL
                  | IGUAL_IGUAL
                  | DIFERENTE'''
    p[0] = p[1]


def p_condicion(p):
    '''condicion : expresion comparador expresion
                 | expresion'''
    if len(p) == 2:
        p[0] = p[1] if isinstance(p[1], bool) else False
    else:
        p[0] = True if type(p[1]) == type(p[3]) else False

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion
                 | NEGACION expresion'''
    if len(p) == 4:
        p[0] = p[1] and p[3] if p[2] == 'AND' else p[1] or p[3]
    else:
        p[0] = not p[2]

def p_valor(p):
    '''valor : NUMERO
             | DECIMAL
             | CADENA
             | IDENTIFICADOR'''
    if p.slice[1].type == "IDENTIFICADOR":
        simbolo = buscar_simbolo(p[1])
        p[0] = simbolo['valor'] if simbolo else None
    else:
        p[0] = p[1]


def p_parametros(p):
    '''parametros : parametro
                  | parametro COMA parametros
                  | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parametro(p):
    '''parametro : NUMERO IDENTIFICADOR
                 | DECIMAL IDENTIFICADOR
                 | BOOLEANO IDENTIFICADOR
                 | CADENA IDENTIFICADOR'''
    tipo = p[1].lower()
    nombre = p[2]
    linea = encontrar_linea(lexer.lexdata, p.slice[2])
    columna = encontrar_columna(lexer.lexdata, p.slice[2])
    p[0] = {'tipo': tipo, 'nombre': nombre, 'linea': linea, 'columna': columna}

def p_argumentos(p):
    '''argumentos : expresion
                  | expresion COMA argumentos
                  | empty'''
    if len(p) == 2:
        p[0] = [] if p[1] is None else [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_sentencia_funcion(p):
    '''sentencia : IDENTIFICADOR PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER'''
    nombre = p[1]
    simbolo = buscar_simbolo(nombre)
    if not simbolo or simbolo["tipo"] != "funcion":
        errores_semanticos.append((f"Error semántico: '{nombre}' no es una función declarada.", encontrar_linea(lexer.lexdata, p.slice[1]), encontrar_columna(lexer.lexdata, p.slice[1])))
    else:
        entrar_ambito(nombre)
        p[0] = p[5]
        salir_ambito()


def p_sentencia_funcion_declaracion(p):
    '''sentencia_funcion_declaracion : FUNCION IDENTIFICADOR PARENIZQ parametros PARENDER LLAVEIZQ sentencias LLAVEDER'''
    nombre_funcion = p[2]
    parametros = p[4]
    cuerpo = p[7]
    linea = encontrar_linea(lexer.lexdata, p.slice[2])
    columna = encontrar_columna(lexer.lexdata, p.slice[2])
    if buscar_simbolo(nombre_funcion):
        errores_semanticos.append((f"Error semántico: La función '{nombre_funcion}' ya ha sido declarada.", linea, columna))
        return
    agregar_simbolo(nombre_funcion, "funcion", None, linea, columna, modificable=False, parametros=parametros)
    entrar_ambito(nombre_funcion)
    for param in parametros:
        agregar_simbolo(param['nombre'], param['tipo'], None, param['linea'], param['columna'])
    salir_ambito()
    p[0] = None

def p_error(p):
    if p:
        lin = encontrar_linea(p.lexer.lexdata, p)
        col = encontrar_columna(p.lexer.lexdata, p)
        errores_sintacticos.append(
            (f"Error de sintaxis: Token inesperado '{p.value}'", lin, col)
        )
    else:
        errores_sintacticos.append(("Error de sintaxis: Fin de archivo inesperado", 0, -1))

parser = yacc.yacc()

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.read()
        print(" Archivo leído correctamente.\n")
        return contenido
    except FileNotFoundError:
        print(" Error: No se encontró el archivo.")
        return None

def detectar_variables_no_utilizadas():
    for clave, datos in tabla_simbolos.items():
        if not datos['usado']:
            nombre = clave.split('_')[0]
            errores_semanticos.append(
                (f"Advertencia: La variable '{nombre}' fue declarada pero no utilizada.", datos['linea'], datos['columna'])
            )

def analizar_sintaxis(contenido):
    lexer.lineno = 1
    lexer.input(contenido)
    lexer.lexdata = contenido

    tokens = []
    errores_lexicos = []

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    # Asigna columna a cada token para el HTML
    for token in tokens:
        token.lineno = encontrar_linea(lexer.lexdata, token)
        token.column = encontrar_columna(lexer.lexdata, token)

    # Mostrar tokens con línea y columna (opcional)
    for token in tokens:
        print(f"Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}, Columna: {token.column}")

    # Volver a alimentar el lexer para el parser
    lexer.input(contenido)

    parser.parse(contenido, lexer=lexer)
    detectar_variables_no_utilizadas()

    html_gen.generar_pagina_inicio()
    html_gen.generar_html_tokens(tokens)
    html_gen.generar_html_errores(errores_lexicos + errores_sintacticos + errores_semanticos)
    html_gen.generar_html_tabla_simbolos(tabla_simbolos)
    html_gen.abrir_html("index.html")