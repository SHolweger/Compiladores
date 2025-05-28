# parser_module.py

import ply.yacc as yacc
from lexer_module import tokens, lexer, analizar_codigo, encontrar_linea, encontrar_columna
from tabla_simbolos import SymbolTable
from ast_nodes import *
from semantic_module import SemanticAnalyzer
from interpreter import Interpreter
import html_gen

# ------------------------------------------------------------
# Precedencia y asociatividad de operadores
# ------------------------------------------------------------
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'IGUAL_IGUAL', 'DIFERENTE'),
    ('left', 'MAYOR', 'MENOR', 'MAYOR_IGUAL', 'MENOR_IGUAL'),
    ('left', 'SUMA', 'RESTA'),
    ('left', 'MULT', 'DIV', 'MOD'),
    ('right', 'NEGACION'),
)

# ------------------------------------------------------------
# Estado global: tabla de símbolos y listas de errores
# ------------------------------------------------------------
tabla = SymbolTable()
errores_lexicos: list = []
errores_sintacticos: list = []

# ------------------------------------------------------------
# Auxiliares línea/columna
# ------------------------------------------------------------
def _line(p, i):
    try:
        tok = p.slice[i]
        return encontrar_linea(lexer.lexdata, tok)
    except:
        return 0

def _col(p, i):
    try:
        tok = p.slice[i]
        return encontrar_columna(lexer.lexdata, tok)
    except:
        return 0

# ------------------------------------------------------------
# Gramática
# ------------------------------------------------------------

def p_programa(p):
    'programa : lista_funciones'
    p[0] = Program(p[1])

def p_lista_funciones(p):
    '''lista_funciones : funcion
                       | funcion lista_funciones'''
    p[0] = [p[1]] if len(p)==2 else [p[1]] + p[2]

def p_funcion_inicio(p):
    'funcion : INICIO PARENIZQ PARENDER bloque_funcion'
    linea, col = _line(p,1), _col(p,1)
    # registrar 'inicio'
    tabla.agregar_simbolo('inicio','funcion', None, linea, col,
                          modificable=False, parametros=[], retorno=None)
    p[0] = FuncDecl('inicio', [], p[4], linea, col)

def p_funcion_normal(p):
    'funcion : FUNCION IDENTIFICADOR PARENIZQ lista_params PARENDER bloque_funcion'
    nombre = p[2]
    linea, col = _line(p,2), _col(p,2)
    params = p[4]
    tabla.agregar_simbolo(nombre,'funcion', None, linea, col,
                          modificable=False,
                          parametros=[(par.nombre,par.tipo) for par in params],
                          retorno=None)
    p[0] = FuncDecl(nombre, params, p[6], linea, col)

def p_lista_params(p):
    '''lista_params :
                    | params_no_vacios'''
    p[0] = [] if len(p)==1 else p[1]

def p_params_no_vacios(p):
    '''params_no_vacios : param
                        | param COMA params_no_vacios'''
    p[0] = [p[1]] if len(p)==2 else [p[1]] + p[3]

def p_param(p):
    'param : tipo IDENTIFICADOR'
    linea, col = _line(p,2), _col(p,2)
    tabla.agregar_simbolo(p[2], p[1], None, linea, col)
    p[0] = Param(p[1], p[2], linea, col)

def p_tipo(p):
    '''tipo : NUMERO
            | DECIMAL
            | BOOLEANO
            | CADENA'''
    p[0] = p[1]

# bloque de función = entra al ámbito, lee llaves, sale
def p_bloque_funcion(p):
    'bloque_funcion : LLAVEIZQ abrir_ambito_funcion sentencias LLAVEDER cerrar_ambito'
    p[0] = p[3]

def p_abrir_ambito_funcion(p):
    'abrir_ambito_funcion :'
    tabla.entrar_ambito("funcion")

def p_cerrar_ambito(p):
    'cerrar_ambito :'
    tabla.salir_ambito()

# bloque genérico para if/while/for/dowhile
def p_bloque(p):
    'bloque : LLAVEIZQ abrir_ambito sentencias LLAVEDER cerrar_ambito'
    p[0] = p[3]

def p_abrir_ambito(p):
    'abrir_ambito :'
    tabla.entrar_ambito("bloque")

def p_sentencias(p):
    '''sentencias : sentencia
                  | sentencia sentencias'''
    p[0] = [p[1]] if len(p)==2 else [p[1]] + p[2]

def p_sentencia_declaracion(p):
    '''sentencia : tipo IDENTIFICADOR IGUAL expresion PUNTOYCOMA
                 | tipo IDENTIFICADOR PUNTOYCOMA'''
    tipo, nombre = p[1], p[2]
    linea, col = _line(p,2), _col(p,2)
    expr = p[4] if len(p)==6 else None
    tabla.agregar_simbolo(nombre, tipo, expr, linea, col)
    p[0] = VarDecl(tipo, nombre, expr, linea, col)

def p_sentencia_asignacion(p):
    'sentencia : IDENTIFICADOR OP_ASIG expresion PUNTOYCOMA'
    p[0] = Assign(p[1], p[2], p[3], _line(p,1), _col(p,1))

def p_OP_ASIG(p):
    '''OP_ASIG : IGUAL
               | SUMA_IGUAL
               | RESTA_IGUAL
               | MULT_IGUAL
               | DIV_IGUAL'''
    p[0] = p[1]

def p_sentencia_llamada(p):
    'sentencia : IDENTIFICADOR PARENIZQ args PARENDER PUNTOYCOMA'
    p[0] = FuncCall(p[1], p[3], _line(p,1), _col(p,1))

def p_args(p):
    '''args :
            | lista_args'''
    p[0] = [] if len(p)==1 else p[1]

def p_lista_args(p):
    '''lista_args : expresion
                  | expresion COMA lista_args'''
    p[0] = [p[1]] if len(p)==2 else [p[1]] + p[3]

def p_expresion_relacional(p):
    '''expresion : expresion IGUAL_IGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion MAYOR expresion
                 | expresion MENOR expresion
                 | expresion MAYOR_IGUAL expresion
                 | expresion MENOR_IGUAL expresion'''
    p[0] = CompareOp(p[1], p[2], p[3], _line(p,2), _col(p,2))

def p_expresion_logica(p):
    '''expresion : expresion AND expresion
                 | expresion OR expresion
                 | NEGACION expresion'''
    if len(p) == 3:
        # !expr
        p[0] = LogicalOp('not', p[2], None, _line(p,1), _col(p,1))
    else:
        # expr && expr  o expr || expr
        p[0] = LogicalOp(p[2].lower(), p[1], p[3], _line(p,2), _col(p,2))

def p_expresion(p):
    '''expresion : expresion SUMA expresion
                 | expresion RESTA expresion
                 | expresion MULT expresion
                 | expresion DIV expresion
                 | expresion MOD expresion
                 | PARENIZQ expresion PARENDER
                 | literal
                 | IDENTIFICADOR
                 | llamada_funcion_expr'''
    if len(p)==2:
        if isinstance(p[1], str):
            p[0] = VarRef(p[1], _line(p,1), _col(p,1))
        else:
            p[0] = p[1]
    elif p[1]=='(':
        p[0] = p[2]
    else:
        p[0] = BinOp(p[1], p[2], p[3], _line(p,2), _col(p,2))

def p_literal(p):
    '''literal : NUMERO
               | DECIMAL
               | CADENA
               | VERDADERO
               | FALSO'''
    val = p[1]
    if isinstance(val, str) and val.lower() in ('verdadero','falso'):
        val = (val.lower()=='verdadero')
    p[0] = Literal(val, _line(p,1), _col(p,1))

def p_llamada_funcion_expr(p):
    'llamada_funcion_expr : IDENTIFICADOR PARENIZQ args PARENDER'
    p[0] = FuncCall(p[1], p[3], _line(p,1), _col(p,1))

def p_sentencia_si(p):
    '''sentencia : SI PARENIZQ expresion PARENDER bloque
                 | SI PARENIZQ expresion PARENDER bloque SINO bloque'''
    if len(p)==6:
        p[0] = IfThen(p[3], p[5], _line(p,1), _col(p,1))
    else:
        p[0] = IfThenElse(p[3], p[5], p[7], _line(p,1), _col(p,1))

def p_sentencia_mientras(p):
    'sentencia : MIENTRAS PARENIZQ expresion PARENDER bloque'
    p[0] = While(p[3], p[5], _line(p,1), _col(p,1))

def p_sentencia_hacer_mientras(p):
    'sentencia : REPETIR bloque HASTA PARENIZQ expresion PARENDER PUNTOYCOMA'
    p[0] = DoWhile(p[2], p[5], _line(p,1), _col(p,1))

def p_sentencia_para(p):
    'sentencia : PARA PARENIZQ for_init PUNTOYCOMA expresion PUNTOYCOMA for_update PARENDER bloque'
    p[0] = ForLoop(p[3], p[5], p[7], p[9], _line(p,1), _col(p,1))

def p_for_init(p):
    '''for_init : tipo IDENTIFICADOR IGUAL expresion
                | IDENTIFICADOR OP_ASIG expresion
                | empty'''
    if len(p)==5:
        linea, col = _line(p,2), _col(p,2)
        tabla.agregar_simbolo(p[2], p[1], p[4], linea, col)
        p[0] = VarDecl(p[1], p[2], p[4], linea, col)
    elif len(p)==4:
        p[0] = Assign(p[1], p[2], p[3], _line(p,1), _col(p,1))
    else:
        p[0] = None

def p_for_update(p):
    '''for_update : IDENTIFICADOR OP_ASIG expresion
                  | empty'''
    if len(p)==4:
        p[0] = Assign(p[1], p[2], p[3], _line(p,1), _col(p,1))
    else:
        p[0] = None

def p_empty(p):
    'empty :'
    pass

def p_sentencia_mostrar(p):
    'sentencia : MOSTRAR PARENIZQ expresion PARENDER PUNTOYCOMA'
    p[0] = Print(p[3], _line(p,1), _col(p,1))

def p_sentencia_regresa(p):
    'sentencia : REGRESA expresion PUNTOYCOMA'
    p[0] = Return(p[2], _line(p,1), _col(p,1))

def p_sentencia_exprstmt(p):
    'sentencia : expresion PUNTOYCOMA'
    p[0] = ExprStmt(p[1])

def p_sentencia_break(p):
    'sentencia : BREAK PUNTOYCOMA'
    p[0] = Break(_line(p,1), _col(p,1))

def p_sentencia_continue(p):
    'sentencia : CONTINUE PUNTOYCOMA'
    p[0] = Continue(_line(p,1), _col(p,1))

def p_error(p):
    if p:
        errores_sintacticos.append(
            (f"Error sintáctico: '{p.value}' inesperado", _line(p,0), _col(p,0))
        )
    else:
        errores_sintacticos.append(("Error sintáctico: fin de archivo inesperado", 0, 0))

# construir parser
parser = yacc.yacc()

def analizar_sintaxis(contenido:str):
    global tabla, errores_lexicos, errores_sintacticos
    # 1) léxico
    tokens_list, errores_lexicos = analizar_codigo(contenido)
    # 2) parse + tabla limpia
    tabla = SymbolTable()
    errores_sintacticos.clear()
    lexer.input(contenido); lexer.lexdata=contenido
    ast = parser.parse(contenido, lexer=lexer)
    if ast is None:
        print("❌ Error: el parser devolvió None")
        print("Errores sintácticos:", errores_sintacticos)
        return

    # 3) semántica
    sem = SemanticAnalyzer(tabla)
    sem_res = sem.analyze(ast)
    errores_sintacticos += sem.get_errors_for_html()
    # 4) interpretación
    Interpreter(tabla).interpret(ast)
    # 5) HTML
    all_errs = errores_lexicos + errores_sintacticos + tabla.errors
    html_gen.generar_pagina_inicio()
    html_gen.generar_html_tokens(tokens_list)
    html_gen.generar_html_errores(list(dict.fromkeys(all_errs)))
    html_gen.generar_html_tabla_simbolos(tabla)
    html_gen.abrir_html("index.html")
    return ast
