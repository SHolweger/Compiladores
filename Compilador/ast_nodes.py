#ast_nodes.py
class ASTNode:
    def __init__(self, linea=0, columna=0):
        self.linea = linea
        self.columna = columna

class Program(ASTNode):
    def __init__(self, sentencias, linea=0, columna=0):
        super().__init__(linea, columna)
        self.sentencias = sentencias

class FuncDecl(ASTNode):
    def __init__(self, name, params, body, linea=0, columna=0):
        super().__init__(linea, columna)
        self.name = name
        self.params = params
        self.body = body

class Param(ASTNode):
    def __init__(self, tipo, nombre, linea=0, columna=0):
        super().__init__(linea, columna)
        self.tipo = tipo
        self.nombre = nombre

class VarDecl(ASTNode):
    def __init__(self, tipo, nombre, expr=None, linea=0, columna=0):
        super().__init__(linea, columna)
        self.tipo = tipo
        self.nombre = nombre
        self.expr = expr

class Assign(ASTNode):
    def __init__(self, nombre, op, expr, linea=0, columna=0):
        super().__init__(linea, columna)
        self.nombre = nombre
        self.op = op
        self.expr = expr

class BinOp(ASTNode):
    def __init__(self, left, op, right, linea=0, columna=0):
        super().__init__(linea, columna)
        self.left = left
        self.op = op
        self.right = right

class LogicalOp(ASTNode):
    def __init__(self, op, left, right=None, linea=0, columna=0):
        super().__init__(linea, columna)
        self.op = op
        self.left = left
        self.right = right

class CompareOp(ASTNode):
    def __init__(self, left, op, right, linea=0, columna=0):
        super().__init__(linea, columna)
        self.left = left
        self.op = op
        self.right = right

class Literal(ASTNode):
    def __init__(self, value, linea=0, columna=0):
        super().__init__(linea, columna)
        self.value = value

class VarRef(ASTNode):
    def __init__(self, nombre, linea=0, columna=0):
        super().__init__(linea, columna)
        self.nombre = nombre

class FuncCall(ASTNode):
    def __init__(self, name, args, linea=0, columna=0):
        super().__init__(linea, columna)
        self.name = name
        self.args = args

class IfThen(ASTNode):
    def __init__(self, cond, then_body, linea=0, columna=0):
        super().__init__(linea, columna)
        self.cond = cond
        self.then_body = then_body

class IfThenElse(ASTNode):
    def __init__(self, cond, then_body, else_body, linea=0, columna=0):
        super().__init__(linea, columna)
        self.cond = cond
        self.then_body = then_body
        self.else_body = else_body

class While(ASTNode):
    def __init__(self, cond, body, linea=0, columna=0):
        super().__init__(linea, columna)
        self.cond = cond
        self.body = body

class DoWhile(ASTNode):
    def __init__(self, body, cond, linea=0, columna=0):
        super().__init__(linea, columna)
        self.body = body
        self.cond = cond

class ForLoop(ASTNode):
    def __init__(self, init, cond, update, body, linea=0, columna=0):
        super().__init__(linea, columna)
        self.init = init
        self.cond = cond
        self.update = update
        self.body = body

class Print(ASTNode):
    def __init__(self, expr, linea=0, columna=0):
        super().__init__(linea, columna)
        self.expr = expr

class Return(ASTNode):
    def __init__(self, expr, linea=0, columna=0):
        super().__init__(linea, columna)
        self.expr = expr

class Break(ASTNode):
    pass

class Continue(ASTNode):
    pass

class ExprStmt(ASTNode):
    def __init__(self, expr, linea=0, columna=0):
        super().__init__(linea, columna)
        self.expr = expr
