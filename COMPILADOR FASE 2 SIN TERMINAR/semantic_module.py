# === semantic_module.py ===
"""
Análisis semántico robusto: chequeo de tipos, usos, retornos, llamadas y control de flujo.
Utiliza la SymbolTable gestionada por el parser.
"""
from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        """Recibe la instancia de SymbolTable con declaraciones cargadas."""
        self.symtab = symbol_table
        self.errors = self.symtab.errors
        self._loop_depth = 0
        self._current_function = None

    def analyze(self, program: Program):
        """Inicia el recorrido semántico sobre el AST de programa."""
        for stmt in program.sentencias:
            self._check_pass(stmt)
        self.symtab.verificar_uso_variables()
        return self.errors

    def _check_pass(self, node):
        # Manejo de Funciones
        if isinstance(node, FuncDecl):
            entry = self.symtab.buscar_simbolo(node.name, node.linea, node.columna)
            prev = self._current_function
            self._current_function = entry
            for stmt in node.body:
                self._check_pass(stmt)
            self._current_function = prev
            return

        # Declaración de variables
        if isinstance(node, VarDecl):
            if node.expr:
                t_expr = self._eval_type(node.expr)
                if t_expr and t_expr != node.tipo:
                    self.errors.append((
                        f"Error Semántico: Inicialización de '{node.nombre}' con tipo '{t_expr}' no coincide con '{node.tipo}'.",
                        node.linea, node.columna
                    ))
                self._check_expr(node.expr)
            return

        # Asignaciones
        if isinstance(node, Assign):
            entry = self.symtab.buscar_simbolo(node.nombre, node.linea, node.columna)
            if entry:
                t_expr = self._eval_type(node.expr)
                if t_expr and t_expr != entry['tipo']:
                    self.errors.append((
                        f"Error Semántico: Asignación de tipo '{t_expr}' a variable '{node.nombre}' de tipo '{entry['tipo']}'.",
                        node.linea, node.columna
                    ))
                self._check_expr(node.expr)
            return

        # Estructuras de control
        if isinstance(node, IfThen) or isinstance(node, IfThenElse):
            nombre = 'si' if isinstance(node, IfThen) else 'si-sino'
            self._check_cond(node.cond, nombre)
            for s in node.then_body:
                self._check_pass(s)
            if isinstance(node, IfThenElse):
                for s in node.else_body:
                    self._check_pass(s)
            return

        if isinstance(node, While):
            self._loop_depth += 1
            self._check_cond(node.cond, 'mientras')
            for s in node.body:
                self._check_pass(s)
            self._loop_depth -= 1
            return

        if isinstance(node, DoWhile):
            self._loop_depth += 1
            for s in node.body:
                self._check_pass(s)
            self._check_cond(node.cond, 'hacer-mientras')
            self._loop_depth -= 1
            return

        if isinstance(node, ForLoop):
            self._loop_depth += 1
            if node.init: self._check_pass(node.init)
            self._check_cond(node.cond, 'para')
            if node.update: self._check_pass(node.update)
            for s in node.body:
                self._check_pass(s)
            self._loop_depth -= 1
            return

        # Return
        if isinstance(node, Return):
            if self._current_function is None:
                self.errors.append((
                    "Error Semántico: 'regresa' fuera de función.",
                    node.linea, node.columna
                ))
            if node.expr is not None:
                t = self._eval_type(node.expr)
                exp = self._current_function.get('retorno') if self._current_function else None
                if exp and t and t != exp:
                    self.errors.append((
                        f"Error Semántico: Return de tipo '{t}' no coincide con '{exp}'.",
                        node.linea, node.columna
                    ))
                self._check_expr(node.expr)
            return

        # Sentencias y expresiones sueltas
        if isinstance(node, ExprStmt): self._check_expr(node.expr); return
        if isinstance(node, Print): self._check_expr(node.expr); return
        if isinstance(node, FuncCall):
            entry = self.symtab.buscar_simbolo(node.name, node.linea, node.columna)
            if entry:
                params = entry.get('parametros') or []
                if len(node.args) != len(params):
                    self.errors.append((
                        f"Error Semántico: Llamada a '{node.name}' con {len(node.args)} args, se esperaban {len(params)}.",
                        node.linea, node.columna
                    ))
                for arg in node.args: self._check_expr(arg)
            return

        # Switch/Case
        if isinstance(node, Switch):
            t_expr = self._eval_type(node.expr)
            self._check_expr(node.expr)
            has_def = False
            for case in node.casos:
                if case.value is None:
                    has_def = True
                else:
                    t_case = self._eval_type(case.value)
                    if t_case and t_case != t_expr:
                        self.errors.append((
                            f"Error Semántico: Case con tipo '{t_case}' no coincide con switch de tipo '{t_expr}'.",
                            case.linea, case.columna
                        ))
                for s in case.body: self._check_pass(s)
            if not has_def:
                self.errors.append((
                    "Error Semántico: Switch sin caso 'predeterminado'.",
                    node.linea, node.columna
                ))
            return

        # Break/Continue
        if isinstance(node, Break) or isinstance(node, Continue):
            if self._loop_depth == 0:
                self.errors.append((
                    f"Error Semántico: '{type(node).__name__}' fuera de bucle.",
                    node.linea, node.columna
                ))
            return

        # Otros nodos no manejados

    def _check_cond(self, expr, nombre):
        # manejar comparaciones tupla (expr1, op, expr2)
        if isinstance(expr, tuple) and len(expr) == 3:
            left, op, right = expr
            t_l = self._eval_type(left)
            t_r = self._eval_type(right)
            # solo error si los tipos de operandos difieren
            if t_l and t_r and t_l != t_r:
                self.errors.append((
                    f"Error Semántico: Comparador '{op}' con operandos de distintos tipos '{t_l}' y '{t_r}'.",
                    getattr(left, 'linea', 0), getattr(left, 'columna', 0)
                ))
            # recorrer subexpresiones
            self._check_expr(left)
            self._check_expr(right)
            return

        # caso normal: expr debe ser booleano
        t = self._eval_type(expr)
        if t != 'booleano':
            self.errors.append((
                f"Error Semántico: Condición de '{nombre}' no es booleano (obtuvo '{t}').",
                getattr(expr, 'linea', 0), getattr(expr, 'columna', 0)
            ))
        # recorrer la expresión
        self._check_expr(expr)

    def _check_expr(self, expr):
        # manejar comparaciones tupla
        if isinstance(expr, tuple) and len(expr) == 3:
            left, op, right = expr
            t_l = self._eval_type(left); t_r = self._eval_type(right)
            if t_l and t_r and t_l != t_r:
                self.errors.append((
                    f"Error Semántico: Operador '{op}' con operandos de distintos tipos '{t_l}' y '{t_r}'.",
                    left.linea, left.columna
                ))
            self._check_expr(left); self._check_expr(right)
            return

        if isinstance(expr, BinOp):
            lt = self._eval_type(expr.left); rt = self._eval_type(expr.right)
            if lt and rt and lt != rt:
                self.errors.append((
                    f"Error Semántico: Operador '{expr.op}' con operandos de distintos tipos '{lt}' y '{rt}'.",
                    getattr(expr, 'linea', 0), getattr(expr, 'columna', 0)
                ))
            self._check_expr(expr.left); self._check_expr(expr.right)
            return

        if isinstance(expr, LogicalOp):
            for sub in (expr.left, expr.right):
                if sub: self._check_expr(sub)
            return

        if isinstance(expr, VarRef):
            self.symtab.buscar_simbolo(expr.nombre, expr.linea, expr.columna)
            return

        if isinstance(expr, FuncCall):
            self._check_pass(expr)
            return

    def _eval_type(self, expr):
        # Literales
        if isinstance(expr, Literal):
            v = expr.value
            if isinstance(v, bool): return 'booleano'
            if isinstance(v, int): return 'numero'
            if isinstance(v, float): return 'decimal'
            if isinstance(v, str): return 'cadena'

        # Comparación como tupla
        if isinstance(expr, tuple) and len(expr) == 3:
            left, op, right = expr
            t_l = self._eval_type(left); t_r = self._eval_type(right)
            if t_l == t_r:
                return 'booleano' if op in ['>', '<', '>=', '<=', '==', '!='] else t_l
            return None

        # Variable por referencia
        if isinstance(expr, VarRef):
            entry = self.symtab.buscar_simbolo(expr.nombre, expr.linea, expr.columna)
            return entry.get('tipo') if entry else None

        if isinstance(expr, BinOp):
            lt = self._eval_type(expr.left); rt = self._eval_type(expr.right)
            if lt == rt:
                if expr.op in ['>', '<', '>=', '<=', '==', '!=']:
                    return 'booleano'
                return lt

        if isinstance(expr, LogicalOp):
            return 'booleano'

        if isinstance(expr, FuncCall):
            entry = self.symtab.buscar_simbolo(expr.name, expr.linea, expr.columna)
            return entry.get('retorno') if entry else None

        return None
