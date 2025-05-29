#interpreter.py
from ast_nodes import *
from tabla_simbolos import SymbolTable

class Interpreter:
    def __init__(self, symbol_table: SymbolTable):
        self.table = symbol_table
        self.env = {}  # nombre -> valor
        self.call_stack = []  # para ambitos de variables locales

    def interpret(self, program: Program):
        # buscar FuncDecl 'inicio' y ejecutarlo
        for stmt in program.sentencias:
            if isinstance(stmt, FuncDecl) and stmt.name == 'inicio':
                # aislamos el entorno al entrar en la función 'inicio'
                self._execute_block(stmt.body, isolate_env=True)
                return

    def _execute_block(self, stmts, isolate_env: bool = False):
        """
        Ejecuta una lista de sentencias.
        Si isolate_env es True, restaura el entorno al finalizar (para funciones).
        """
        if isolate_env:
            old_env = self.env.copy()
        for s in stmts:
            result = self._exec(s)
            if isinstance(result, Return):  # detener al regresar
                break
        if isolate_env:
            self.env = old_env

    def _exec(self, node):
        name = type(node).__name__.lower()
        method = f'_exec_{name}'
        if hasattr(self, method):
            return getattr(self, method)(node)

    def _exec_vardecl(self, node: VarDecl):
        val = self._eval(node.expr) if node.expr else None
        self.env[node.nombre] = val
        self.table.actualizar_simbolo(node.nombre, val, node.linea, node.columna)

    def _exec_assign(self, node: Assign):
        val = self._eval(node.expr)
        if node.op == '=':
            new = val
        else:
            old = self.env.get(node.nombre)
            op = node.op[0]
            ops = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'truediv'}
            new = getattr(old, f'__{ops[op]}__')(val)
        self.env[node.nombre] = new
        self.table.actualizar_simbolo(node.nombre, new, node.linea, node.columna)

    def _exec_print(self, node: Print):
        val = self._eval(node.expr)
        print(val)

    def _exec_ifthen(self, node: IfThen):
        if self._eval(node.cond):
            # no aislamos para que cambios persistan
            self._execute_block(node.then_body)

    def _exec_ifthenelse(self, node: IfThenElse):
        if self._eval(node.cond):
            self._execute_block(node.then_body)
        else:
            self._execute_block(node.else_body)

    def _exec_while(self, node: While):
        while self._eval(node.cond):
            # no aislamos para que i++ persista
            self._execute_block(node.body)

    def _exec_dowhile(self, node: DoWhile):
        while True:
            self._execute_block(node.body)
            if not self._eval(node.cond):
                break

    def _exec_forloop(self, node: ForLoop):
        if node.init:
            self._exec(node.init)
        while True:
            if node.cond and not self._eval(node.cond):
                break
            self._execute_block(node.body)
            if node.update:
                self._exec(node.update)

    def _exec_return(self, node: Return):
        # señal de retorno
        return node

    def _exec_break(self, node: Break):
        raise RuntimeError("break no soportado en interpretación directa")

    def _exec_continue(self, node: Continue):
        raise RuntimeError("continue no soportado en interpretación directa")

    def _eval(self, node):
        if node is None:
            return None
        type_name = type(node).__name__.lower()
        method = f'_eval_{type_name}'
        if hasattr(self, method):
            return getattr(self, method)(node)
        return None

    def _eval_literal(self, node: Literal):
        return node.value

    def _eval_varref(self, node: VarRef):
        return self.env.get(node.nombre)

    def _eval_binop(self, node: BinOp):
        l = self._eval(node.left)
        r = self._eval(node.right)
        ops = {'+': l + r, '-': l - r, '*': l * r, '/': l / r, '%': l % r}
        return ops.get(node.op)

    def _eval_compareop(self, node: CompareOp):
        l = self._eval(node.left)
        r = self._eval(node.right)
        ops = {
            '==': l == r, '!=': l != r,
            '<': l < r, '>': l > r,
            '<=': l <= r, '>=': l >= r
        }
        return ops.get(node.op)

    def _eval_logicalop(self, node: LogicalOp):
        if node.op == 'not':
            return not self._eval(node.left)
        left = self._eval(node.left)
        right = self._eval(node.right)
        if node.op == 'and':
            return left and right
        if node.op == 'or':
            return left or right
        return None