# === ast_nodes.py ===
"""
Definición de nodos para el AST.
Cada nodo lleva atributos útiles para el análisis semántico (línea, columna, ámbito opcional).
"""

class Program:
    def __init__(self, sentencias):
        self.sentencias = sentencias

class VarDecl:
    def __init__(self, tipo, nombre, expr, linea, columna):
        self.tipo = tipo
        self.nombre = nombre
        self.expr = expr
        self.linea = linea
        self.columna = columna

class Assign:
    def __init__(self, nombre, op, expr, linea, columna):
        self.nombre = nombre
        self.op = op
        self.expr = expr
        self.linea = linea
        self.columna = columna

class IfThen:
    def __init__(self, cond, then_body, linea, columna):
        self.cond = cond
        self.then_body = then_body
        self.linea = linea
        self.columna = columna

class IfThenElse(IfThen):
    def __init__(self, cond, then_body, else_body, linea, columna):
        super().__init__(cond, then_body, linea, columna)
        self.else_body = else_body

class While:
    def __init__(self, cond, body, linea, columna):
        self.cond = cond
        self.body = body
        self.linea = linea
        self.columna = columna

class DoWhile(While):
    def __init__(self, body, cond, linea, columna):
        super().__init__(cond, body, linea, columna)

class ForLoop:
    def __init__(self, init, cond, update, body, linea, columna):
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body
        self.linea = linea
        self.columna = columna

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Literal:
    def __init__(self, value):
        self.value = value

class VarRef:
    def __init__(self, nombre, linea, columna):
        self.nombre = nombre
        self.linea = linea
        self.columna = columna

class Print:
    def __init__(self, expr, linea, columna):
        self.expr = expr
        self.linea = linea
        self.columna = columna

class Return:
    def __init__(self, expr, linea, columna):
        self.expr = expr
        self.linea = linea
        self.columna = columna

class ExprStmt:
    def __init__(self, expr):
        self.expr = expr

class LogicalOp:
    def __init__(self, op, left, right=None):
        self.op = op        # 'and', 'or', 'not'
        self.left = left
        self.right = right

# Nodo para menú de usuario
class Menu:
    def __init__(self, opciones, linea, columna):
        self.opciones = opciones
        self.linea = linea
        self.columna = columna

class Option:
    def __init__(self, numero, action, linea, columna):
        self.numero = numero
        self.action = action
        self.linea = linea
        self.columna = columna

# Nodo para switch/case
class Switch:
    def __init__(self, expr, casos, linea, columna):
        self.expr = expr
        self.casos = casos
        self.linea = linea
        self.columna = columna

class Case:
    def __init__(self, value, body, linea, columna):
        self.value = value
        self.body = body
        self.linea = linea
        self.columna = columna

class Default(Case):
    def __init__(self, body, linea, columna):
        super().__init__(None, body, linea, columna)

# Nodos de función
class Param:
    def __init__(self, tipo, nombre, linea, columna):
        self.tipo = tipo
        self.nombre = nombre
        self.linea = linea
        self.columna = columna

class FuncDecl:
    def __init__(self, name, params, body, linea, columna):
        self.name = name
        self.params = params
        self.body = body
        self.linea = linea
        self.columna = columna

class FuncCall:
    def __init__(self, name, args, linea, columna):
        self.name = name
        self.args = args
        self.linea = linea
        self.columna = columna

# Break y continue
class Break:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna

class Continue:
    def __init__(self, linea, columna):
        self.linea = linea
        self.columna = columna
