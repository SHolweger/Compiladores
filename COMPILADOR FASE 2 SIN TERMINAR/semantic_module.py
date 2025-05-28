# semantic_module.py

from ast_nodes import *

class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.errors = []
        self.warnings = []
        self.current_function = None
        self.loop_depth = 0
        self.function_definitions = {}

        # Estadísticas
        self.variables_declared = 0
        self.variables_used = 0
        self.functions_declared = 0
        self.functions_called = 0

    def analyze(self, ast_root: Program):
        """Ejecuta el análisis semántico completo sobre el AST."""
        # Reiniciar estado
        self.errors.clear()
        self.warnings.clear()
        self.function_definitions.clear()
        self.variables_declared = 0
        self.variables_used = 0
        self.functions_declared = 0
        self.functions_called = 0

        # 1) Recolectar las funciones declaradas en la tabla de símbolos
        self._collect_functions()

        # 2) Recorrer el AST
        self._visit(ast_root)

        # 3) Verificar variables no usadas
        self._check_unused_variables()

        return {
            'errors': self.errors,
            'warnings': self.warnings,
            'statistics': self._get_statistics()
        }

    def _collect_functions(self):
        """Busca en la tabla de símbolos todas las funciones declaradas."""
        for (name, scope), meta in self.symbol_table.tabla_simbolos.items():
            if meta['tipo'] == 'funcion':
                self.function_definitions[name] = {
                    'params': meta.get('parametros', []),
                    'return_type': meta.get('retorno', None),
                    'called': False,
                    'has_return': False,
                    'line': meta['linea'],
                    'column': meta['columna']
                }
                self.functions_declared += 1

    def _visit(self, node):
        """Dispatcher genérico según el tipo de nodo."""
        if node is None:
            return None
        method = f"_visit_{type(node).__name__.lower()}"
        visitor = getattr(self, method, None)
        if visitor:
            return visitor(node)
        # nodos sin acción semántica particular
        return None

    def _visit_program(self, node: Program):
        for stmt in node.sentencias:
            self._visit(stmt)

    def _visit_funcdecl(self, node: FuncDecl):
        old_fn = self.current_function
        self.current_function = node.name
        # Verificar que no se declare dos veces (ya en tabla)
        # Recorrer parámetros
        for param in node.params:
            # marcar declaración
            self.variables_declared += 1
        # Recorrer cuerpo
        for stmt in node.body:
            self._visit(stmt)
        self.current_function = old_fn

    def _visit_vardecl(self, node: VarDecl):
        # Cuenta variable declarada
        self.variables_declared += 1
        # Analizar inicializador si existe
        if node.expr:
            self._visit(node.expr)

    def _visit_assign(self, node: Assign):
        # Verificar existencia y marcar uso
        found = self.symbol_table.buscar_simbolo(node.nombre, node.linea, node.columna)
        if found:
            self.variables_used += 1
        # Analizar expresión
        self._visit(node.expr)

    def _visit_varref(self, node: VarRef):
        found = self.symbol_table.buscar_simbolo(node.nombre, node.linea, node.columna)
        if found:
            self.variables_used += 1
            return found['tipo']
        return None

    def _visit_literal(self, node: Literal):
        if isinstance(node.value, bool):
            return 'booleano'
        if isinstance(node.value, int):
            return 'numero'
        if isinstance(node.value, float):
            return 'decimal'
        if isinstance(node.value, str):
            return 'cadena'
        return None

    def _visit_binop(self, node: BinOp):
        lt = self._visit(node.left)
        rt = self._visit(node.right)
        if lt and rt:
            if not self._types_compatible(lt, rt, node.op):
                self._add_error(
                    f"Tipos incompatibles en operación '{node.op}': {lt} vs {rt}",
                    node.linea, node.columna
                )
        return lt or rt

    def _visit_compareop(self, node: CompareOp):
        lt = self._visit(node.left)
        rt = self._visit(node.right)
        if lt and rt:
            if not self._types_compatible(lt, rt, node.op):
                self._add_error(
                    f"Tipos incompatibles en comparación '{node.op}': {lt} vs {rt}",
                    node.linea, node.columna
                )
        return 'booleano'

    def _visit_logicalop(self, node: LogicalOp):
        # ignoramos op de corto circuito; solo chequeamos subexpresiones
        self._visit(node.left)
        if node.right:
            self._visit(node.right)
        return 'booleano'

    def _visit_funccall(self, node: FuncCall):
        if node.name not in self.function_definitions:
            self._add_error(
                f"Función '{node.name}' no declarada",
                node.linea, node.columna
            )
        else:
            # marcar llamada
            self.function_definitions[node.name]['called'] = True
            self.functions_called += 1
        # analizar argumentos
        for arg in node.args:
            self._visit(arg)
        return self.function_definitions.get(node.name, {}).get('return_type', None)

    def _visit_ifthen(self, node: IfThen):
        ctype = self._visit(node.cond)
        for stmt in node.then_body:
            self._visit(stmt)

    def _visit_ifthenelse(self, node: IfThenElse):
        self._visit(node.cond)
        for stmt in node.then_body:
            self._visit(stmt)
        for stmt in node.else_body:
            self._visit(stmt)

    def _visit_while(self, node: While):
        self.loop_depth += 1
        self._visit(node.cond)
        for stmt in node.body:
            self._visit(stmt)
        self.loop_depth -= 1

    def _visit_dowhile(self, node: DoWhile):
        self.loop_depth += 1
        for stmt in node.body:
            self._visit(stmt)
        self._visit(node.cond)
        self.loop_depth -= 1

    def _visit_forloop(self, node: ForLoop):
        self.loop_depth += 1
        if node.init:
            self._visit(node.init)
        if node.cond:
            self._visit(node.cond)
        if node.update:
            self._visit(node.update)
        for stmt in node.body:
            self._visit(stmt)
        self.loop_depth -= 1

    def _visit_print(self, node: Print):
        self._visit(node.expr)

    def _visit_return(self, node: Return):
        if node.expr:
            self._visit(node.expr)
        # marcar que la función actual tiene return
        if self.current_function:
            self.function_definitions[self.current_function]['has_return'] = True

    def _visit_exprstmt(self, node: ExprStmt):
        self._visit(node.expr)

    def _visit_break(self, node: Break):
        if self.loop_depth == 0:
            self._add_error("break fuera de bucle", node.linea, node.columna)

    def _visit_continue(self, node: Continue):
        if self.loop_depth == 0:
            self._add_error("continue fuera de bucle", node.linea, node.columna)

    def _check_unused_variables(self):
        """Genera advertencias para variables no usadas."""
        for (name, scope), meta in self.symbol_table.tabla_simbolos.items():
            if meta['tipo'] != 'funcion' and not meta.get('usado', False):
                self._add_warning(
                    f"Variable '{name}' declarada pero no usada en ámbito '{scope}'",
                    meta['linea'], meta['columna']
                )

    def _types_compatible(self, t1, t2, op):
        """Comprueba compatibilidad básica de tipos."""
        if t1 == t2:
            return True
        numeric = {'numero', 'decimal'}
        if t1 in numeric and t2 in numeric:
            return True
        return False

    def _add_error(self, msg, line, col):
        self.errors.append((f"Error Semántico: {msg}", line, col))

    def _add_warning(self, msg, line, col):
        self.warnings.append((f"Advertencia Semántica: {msg}", line, col))

    def _get_statistics(self):
        return {
            'variables_declared': self.variables_declared,
            'variables_used': self.variables_used,
            'functions_declared': self.functions_declared,
            'functions_called': self.functions_called
        }

    def get_errors_for_html(self):
        """Combina errores y advertencias para reporte."""
        return self.errors + self.warnings
