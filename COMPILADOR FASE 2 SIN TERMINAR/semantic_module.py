# === semantic_module.py ===
"""
Segundo pase: análisis semántico recorriendo el AST y llenando tabla de símbolos.
"""
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self,symbol_table):
        self.table = symbol_table
        self.errors = []
        self.scopes = ['global']

    def enter_scope(self, name):
        self.scopes.append(name)

    def exit_scope(self):
        self.scopes.pop()

    def current_scope(self):
        return self.scopes[-1]

    def analyze(self, program: Program):
        # Pase 1: declaraciones
        #for node in program.sentencias:
        #    if isinstance(node, VarDecl):
        #        self.declare_var(node)
        # Pase 2: usos y tipos
        for node in program.sentencias:
            self.check_node(node)
        # Chequeo de variables no usadas
        self.check_unused_variables()
        return self.errors

    def declare_var(self, node: VarDecl):
        key = (node.nombre, self.current_scope())
        if key in self.table:
            self.errors.append((f"Variable '{node.nombre}' redeclarada.", node.linea, node.columna))
        else:
            self.table[key] = {
                'tipo': node.tipo,
                'valor': None,
                'linea': node.linea,
                'columna': node.columna,
                'ambito': self.current_scope(),
                'modificable': True,
                'usado': False
            }

    def find_decl_scope(self, nombre):
        # Buscar ambito en stack
        for scope in reversed(self.scopes):
            if (nombre, scope) in self.table:
                return scope
        return None

    def check_node(self, node):
        # Despacha según tipo de nodo
        if isinstance(node, Assign):
            self.check_assign(node)
        elif isinstance(node, VarDecl):
            # verificar expresión inicial
            self.check_expr(node.expr)
        elif isinstance(node, IfThen):
            self.check_expr(node.cond)
            for s in node.then_body:
                self.check_node(s)
        elif isinstance(node, IfThenElse):
            self.check_expr(node.cond)
            for s in node.then_body: self.check_node(s)
            for s in node.else_body: self.check_node(s)
        elif isinstance(node, While) or isinstance(node, DoWhile):
            self.check_expr(node.cond)
            for s in node.body: self.check_node(s)
        elif isinstance(node, ForLoop):
            self.check_node(node.init)
            self.check_expr(node.cond)
            self.check_node(node.update)
            for s in node.body: self.check_node(s)
        # ... agregar otros nodos según necesidad

    def check_assign(self, node: Assign):
        scope = self.find_decl_scope(node.nombre)
        if not scope:
            self.errors.append((f"Variable '{node.nombre}' no declarada.", node.linea, node.columna))
        else:
            meta = self.table[(node.nombre, scope)]
            if not meta['modificable']:
                self.errors.append((f"Variable '{node.nombre}' no modificable.", node.linea, node.columna))
            # check expr
            val_type = self.eval_expr_type(node.expr)
            if val_type and val_type != meta['tipo']:
                self.errors.append((f"Asignación de tipo '{val_type}' a '{meta['tipo']}'.", node.linea, node.columna))
            meta['usado'] = True

    def check_expr(self, expr):
        # Recorrer expresiones para detectar uso de variables
        if isinstance(expr, BinOp):
            self.check_expr(expr.left)
            self.check_expr(expr.right)
        elif isinstance(expr, VarRef):
            scope = self.find_decl_scope(expr.nombre)
            if not scope:
                self.errors.append((f"Variable '{expr.nombre}' no declarada.", expr.linea, expr.columna))
            else:
                self.table[(expr.nombre, scope)]['usado'] = True
        # literales no necesitan chequeo

    def eval_expr_type(self, expr):
        if isinstance(expr, Literal):
            return ('numero' if isinstance(expr.value, int)
                    else 'decimal' if isinstance(expr.value, float)
                    else 'cadena' if isinstance(expr.value, str)
                    else 'booleano')
        elif isinstance(expr, VarRef):
            scope = self.find_decl_scope(expr.nombre)
            return self.table[(expr.nombre, scope)]['tipo']
        elif isinstance(expr, BinOp):
            lt = self.eval_expr_type(expr.left)
            rt = self.eval_expr_type(expr.right)
            if lt == rt:
                return lt
        return None

    def check_unused_variables(self):
        for (nombre, ambito), meta in self.table.items():
            if not meta.get('usado', False):
                self.errors.append((f"Advertencia semántica: Variable '{nombre}' declarada en ámbito '{ambito}' pero no usada.", meta['linea'], meta['columna']))
