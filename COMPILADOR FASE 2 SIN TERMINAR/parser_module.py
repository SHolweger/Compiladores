#Parser_module.py
import ply.yacc as yacc
from lexer_module import tokens, lexer, encontrar_columna, encontrar_linea
import html_gen
from tabla_simbolos import SymbolTable
from ast_nodes import *
from semantic_module import SemanticAnalyzer

# ----------------------------------------------------------------------------
# Tabla de símbolos y colecciones de errore
# ----------------------------------------------------------------------------
tabla = SymbolTable()
errores_lexicos = []
errores_sintacticos = []
pila_ambitos = []

# ----------------------------------------------------------------------------
# Precedencia de operadores
# ----------------------------------------------------------------------------
global precedence
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NEGACION'),
)
# === Reglas de gramática que construyen el AST ===

def p_programa(p):
    '''programa : lista_funciones'''
    p[0] = Program(p[1])

def p_lista_funciones(p):
    '''lista_funciones : funcion
                       | funcion lista_funciones'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_funcion(p):
    '''funcion : INICIO PARENIZQ PARENDER LLAVEIZQ sentencias LLAVEDER
               | FUNCION IDENTIFICADOR PARENIZQ params PARENDER abrir_ambito bloque cerrar_ambito'''
    if p[1] == 'inicio':
        p[0] = Program(p[5])
    else:
        nombre = p[2]
        linea = encontrar_linea(lexer.lexdata, p.slice[2])
        col = encontrar_columna(lexer.lexdata, p.slice[2])
        for param in p[4]:
            tabla.agregar_simbolo(param.nombre, param.tipo, None, param.linea, param.columna)
        cuerpo = p[7]
        p[0] = FuncDecl(name=nombre, params=p[4], body=cuerpo, linea=linea, columna=col)
    

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]

# Declaración de variable con inicialización

def p_sentencia_declaracion(p):
    '''sentencia : NUMERO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | DECIMAL IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | BOOLEANO IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | CADENA IDENTIFICADOR IGUAL expresion PUNTOYCOMA'''
    tipo, nombre, expr = p[1].lower(), p[2], p[4]
    linea = encontrar_linea(lexer.lexdata, p.slice[2])
    col = encontrar_columna(lexer.lexdata, p.slice[2])
    p[0] = VarDecl(tipo, nombre, expr, linea, col)
    tabla.agregar_simbolo(nombre, tipo, expr, linea, col)

# Asignación, soportando operadores compuestos

def p_sentencia_asignacion(p):
    'sentencia : IDENTIFICADOR OP_ASIG expresion PUNTOYCOMA'
    nombre, op, expr = p[1], p[2], p[3]
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Assign(nombre, op, expr, linea, col)
    tabla.actualizar_simbolo(nombre, expr, linea, col)

def p_OP_ASIG(p):
    '''OP_ASIG : IGUAL
               | SUMA_IGUAL
               | RESTA_IGUAL
               | MULT_IGUAL
               | DIV_IGUAL'''
    p[0] = p[1]

# SENTENCIA DE RETORNO (REGRESA)
def p_sentencia_regresa(p):
    'sentencia : REGRESA expresion PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Return(p[2], linea, col)           # Nodo AST Return

# If-Then y If-Then-Else
def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ condicion PARENDER abrir_ambito bloque cerrar_ambito
                 | SI PARENIZQ condicion PARENDER abrir_ambito bloque cerrar_ambito SINO abrir_ambito bloque cerrar_ambito'''
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    if len(p) == 8:
        p[0] = IfThen(p[3], p[6], linea, col)
    else:
        p[0] = IfThenElse(p[3], p[6], p[10], linea, col)


# While loop
def p_sentencia_mientras(p):
    'sentencia : MIENTRAS PARENIZQ condicion PARENDER abrir_ambito bloque cerrar_ambito'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = While(p[3], p[6], linea, col)

# Do-While loop
def p_sentencia_hacer_mientras(p):
    'sentencia : REPETIR abrir_ambito bloque cerrar_ambito HASTA PARENIZQ condicion PARENDER PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = DoWhile(p[3], p[7], linea, col)

def p_sentencia_repetir(p):
    'sentencia : REPETIR sentencias HASTA PARENIZQ condicion PARENDER PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = DoWhile(p[2], p[5], linea, col)    # Nodo AST DoWhile

# FOR LOOP (PARA)
def p_for_init(p):
    '''for_init : NUMERO IDENTIFICADOR IGUAL expresion
                | DECIMAL IDENTIFICADOR IGUAL expresion
                | BOOLEANO IDENTIFICADOR IGUAL expresion
                | CADENA IDENTIFICADOR IGUAL expresion
                | IDENTIFICADOR OP_ASIG expresion
                | empty'''
    # Puedes devolver un nodo AST o None
    if len(p) == 5:
        tipo, nombre, expr = p[1].lower(), p[2], p[4]
        linea = encontrar_linea(lexer.lexdata, p.slice[2])
        col = encontrar_columna(lexer.lexdata, p.slice[2])
        p[0] = VarDecl(tipo, nombre, expr, linea, col)
        tabla.agregar_simbolo(nombre, tipo, expr, linea, col)
    elif len(p) == 4:
        nombre, op, expr = p[1], p[2], p[3]
        linea = encontrar_linea(lexer.lexdata, p.slice[1])
        col = encontrar_columna(lexer.lexdata, p.slice[1])
        p[0] = Assign(nombre, op, expr, linea, col)
        tabla.actualizar_simbolo(nombre, expr, linea, col)
    else:
        p[0] = None

def p_for_update(p):
    '''for_update : IDENTIFICADOR OP_ASIG expresion
                  | empty'''
    if len(p) == 4:
        nombre, op, expr = p[1], p[2], p[3]
        linea = encontrar_linea(lexer.lexdata, p.slice[1])
        col = encontrar_columna(lexer.lexdata, p.slice[1])
        p[0] = Assign(nombre, op, expr, linea, col)
        tabla.actualizar_simbolo(nombre, expr, linea, col)
    else:
        p[0] = None

def p_empty(p):
    'empty :'
    pass

def p_sentencia_para(p):
    '''sentencia : PARA PARENIZQ for_init PUNTOYCOMA condicion PUNTOYCOMA for_update PARENDER abrir_ambito bloque cerrar_ambito'''
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = ForLoop(p[3], p[5], p[7], p[10], linea, col)
    #p[0] = ForLoop(p[3], p[4], p[6], p[10], linea, col)si

# EXPRESSIONS STATEMENT (para permitir llamadas a función o cálculos sueltos terminados en ;) 
def p_sentencia_exprstmt(p):
    'sentencia : expresion PUNTOYCOMA'
    # si tienes un AST ExprStmt, úsalo; si no, descártala o envuélvela:
    p[0] = ExprStmt(p[1])
# Asignacion
#def p_asignacion(p):
#    'asignacion : IDENTIFICADOR OP_ASIG expresion PUNTOYCOMA'
#    linea = encontrar_linea(lexer.lexdata, p.slice[1])
#    col   = encontrar_columna(lexer.lexdata, p.slice[1])
#    p[0] = Assign(nombre=p[1], op=p[2], expr=p[3], linea=linea, columna=col)


# Expresiones aritméticas y literales
def p_expresion(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion
                 | PARENIZQ expresion PARENDER
                 | NUMERO
                 | DECIMAL
                 | CADENA
                 | IDENTIFICADOR'''
    if len(p) == 2:
        if isinstance(p[1], (int, float, str)):
            p[0] = Literal(p[1])
        elif isinstance(p[1], str):  # IDENTIFICADOR
            nombre = p[1]
            linea = encontrar_linea(lexer.lexdata, p.slice[1])
            col = encontrar_columna(lexer.lexdata, p.slice[1])
            p[0] = VarRef(nombre, linea, col)
            tabla.buscar_simbolo(nombre, linea, col)
    elif p.slice[1].type == 'PARENIZQ':
        p[0] = p[2]
    else:
        p[0] = BinOp(p[1], p[2], p[3])

# Comparadores y condición

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
        p[0] = p[1]
    else:
        p[0] = (p[1], p[2], p[3])   

# -------------------------
# Menú de usuario
# -------------------------
def p_sentencia_menu(p):
    'sentencia : MENU LLAVEIZQ opciones LLAVEDER'
    p[0] = Menu(p[3], 
                encontrar_linea(lexer.lexdata, p.slice[1]),
                encontrar_columna(lexer.lexdata, p.slice[1]))

def p_opciones(p):
    '''opciones : opcion
                | opciones opcion'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_opcion(p):
    'opcion : NUMERO DOSPUNTOS llamada_accion PUNTOYCOMA'
    p[0] = Option(p[1], p[3],
                  encontrar_linea(lexer.lexdata, p.slice[1]),
                  encontrar_columna(lexer.lexdata, p.slice[1]))

def p_llamada_accion(p):
    '''llamada_accion : MOSTRAR PARENIZQ expresion PARENDER PUNTOYCOMA
                      | IDENTIFICADOR PARENIZQ args PARENDER PUNTOYCOMA'''
    # aquí devuelves el nodo AST que corresponda:
    if p.slice[1].type == 'MOSTRAR':
        p[0] = Print(p[3],
                     encontrar_linea(lexer.lexdata, p.slice[1]),
                     encontrar_columna(lexer.lexdata, p.slice[1]))
    else:
        p[0] = FuncCall(name=p[1], args=p[3],
                        linea=encontrar_linea(lexer.lexdata, p.slice[1]),
                        columna=encontrar_columna(lexer.lexdata, p.slice[1]))

# -------------------------
# Mostrar / Print
# -------------------------
def p_sentencia_mostrar(p):
    'sentencia : MOSTRAR PARENIZQ expresion PARENDER PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Print(p[3], linea, col)

# -------------------------
# Switch / Case
# -------------------------
def p_sentencia_switch(p):
    'sentencia : CAMBIAR PARENIZQ expresion PARENDER LLAVEIZQ casos LLAVEDER'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Switch(p[3], p[7], linea, col)

def p_casos(p):
    '''casos : caso
             | caso casos'''
    p[0] = [p[1]] if len(p) == 2 else [p[1]] + p[2]
def p_caso(p):
    '''caso : CASO expresion DOSPUNTOS abrir_ambito sentencias cerrar_ambito
            | PREDETERMINADO DOSPUNTOS abrir_ambito sentencias cerrar_ambito'''
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col = encontrar_columna(lexer.lexdata, p.slice[1])
    if p.slice[1].type == 'CASO':
        p[0] = Case(p[2], p[5], linea, col)
    else:
        p[0] = Default(p[4], linea, col)

# AMBITOS
def p_abrir_ambito(p):
    'abrir_ambito :'
    tabla.entrar_ambito()

def p_cerrar_ambito(p):
    'cerrar_ambito :'
    tabla.salir_ambito()

def p_bloque(p):
    'bloque : LLAVEIZQ abrir_ambito sentencias cerrar_ambito LLAVEDER'
    p[0] = p[3]

# -------------------------
# Funciones y procedimientos
# -------------------------
def p_sentencia_funcion_declaracion(p):
    'sentencia : FUNCION IDENTIFICADOR PARENIZQ params PARENDER abrir_ambito bloque cerrar_ambito'
    nombre = p[2]
    linea = encontrar_linea(lexer.lexdata, p.slice[2])
    col = encontrar_columna(lexer.lexdata, p.slice[2])
    # Agregar los parámetros al ámbito de la función
    for param in p[4]:
        tabla.agregar_simbolo(param.nombre, param.tipo, None, param.linea, param.columna)
    cuerpo = p[7]
    p[0] = FuncDecl(name=nombre, params=p[4], body=cuerpo, linea=linea, columna=col)
    

def p_params(p):
    '''params :
              | lista_params'''
    p[0] = [] if len(p) == 2 and p[1] is None else p[1]

def p_lista_params(p):
    '''lista_params : tipo IDENTIFICADOR
                    | IDENTIFICADOR
                    | tipo IDENTIFICADOR COMA lista_params
                    | IDENTIFICADOR COMA lista_params'''
    if len(p) == 3 and isinstance(p[1], str) and p[1] in ['numero', 'decimal', 'booleano', 'cadena']:
        param = Param(tipo=p[1].lower(), nombre=p[2],
                      linea=encontrar_linea(lexer.lexdata, p.slice[2]),
                      columna=encontrar_columna(lexer.lexdata, p.slice[2]))
        p[0] = [param]
    elif len(p) == 2:
        param = Param(tipo=None, nombre=p[1],
                      linea=encontrar_linea(lexer.lexdata, p.slice[1]),
                      columna=encontrar_columna(lexer.lexdata, p.slice[1]))
        p[0] = [param]
    else:
        # Recursivo para ambos casos
        if p[1] in ['numero', 'decimal', 'booleano', 'cadena']:
            param = Param(tipo=p[1].lower(), nombre=p[2],
                          linea=encontrar_linea(lexer.lexdata, p.slice[2]),
                          columna=encontrar_columna(lexer.lexdata, p.slice[2]))
            p[0] = [param] + p[4]
        else:
            param = Param(tipo=None, nombre=p[1],
                          linea=encontrar_linea(lexer.lexdata, p.slice[1]),
                          columna=encontrar_columna(lexer.lexdata, p.slice[1]))
            p[0] = [param] + p[3]

def p_tipo(p):
    '''tipo : NUMERO
            | DECIMAL
            | BOOLEANO
            | CADENA'''
    p[0] = p[1].lower()

def p_sentencia_llamada_funcion(p):
    'sentencia : IDENTIFICADOR PARENIZQ args PARENDER PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = FuncCall(name=p[1], args=p[3], linea=linea, columna=col)

def p_args(p):
    '''args : 
            | lista_args'''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = p[1]

def p_lista_args(p):
    '''lista_args : expresion
                  | expresion COMA lista_args'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# -------------------------
# Break y Continue
# -------------------------
def p_sentencia_break(p):
    'sentencia : BREAK PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Break(linea, col)

def p_sentencia_continue(p):
    'sentencia : CONTINUE PUNTOYCOMA'
    linea = encontrar_linea(lexer.lexdata, p.slice[1])
    col   = encontrar_columna(lexer.lexdata, p.slice[1])
    p[0] = Continue(linea, col)


# BOOLEANOS Y LÓGICA
# ----------------------------------------------------------------------------
def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion
                 | NEGACION expresion'''
    if len(p) == 4:
        if p[2] == '&&':
            p[0] = LogicalOp('and', p[1], p[3])
        else:
            p[0] = LogicalOp('or',  p[1], p[3])
    else:
        p[0] = LogicalOp('not', p[2], None)

def p_booleano(p):
    '''expresion : VERDADERO
                 | FALSO'''
    value = True if p[1].lower() == 'verdadero' else False
    p[0] = Literal(value)



# Errores sintácticos
def p_error(p):
    if p:
        linea = encontrar_linea(p.lexer.lexdata, p)
        col = encontrar_columna(p.lexer.lexdata, p)
        errores_sintacticos.append((f"Error sintáctico: '{p.value}' inesperado", linea, col))
    else:
        errores_sintacticos.append(("Error sintáctico: fin de archivo inesperado", 0, 0))

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

def analizar_sintaxis(contenido):
    lexer.errores = []
    lexer.lineno = 1
    lexer.input(contenido)
    lexer.lexdata = contenido

    tokens = []
    errores_lexicos = lexer.errores

    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)

    
    for token in tokens:
        token.lineno = encontrar_linea(lexer.lexdata, token)
        token.column = encontrar_columna(lexer.lexdata, token)

    # Mostrar tokens con línea y columna (opcional)
    for token in tokens:
        print(f"Token: {token.type}, Valor: {token.value}, Línea: {token.lineno}, Columna: {token.column}")
    # Volver a alimentar el lexer para el parser
    lexer.input(contenido)
    
    ast = parser.parse(contenido, lexer=lexer)
    
    # ANÁLISIS SEMÁNTICO
    errores_semanticos = []
    if ast:
        sema = SemanticAnalyzer(tabla.tabla_simbolos)
        errores_semanticos = sema.analyze(ast)
    
    
    html_gen.generar_pagina_inicio()
    html_gen.generar_html_tokens(tokens)
    html_gen.generar_html_errores(errores_lexicos + errores_sintacticos + errores_semanticos)
    html_gen.generar_html_tabla_simbolos(tabla.tabla_simbolos)
    html_gen.abrir_html("index.html")