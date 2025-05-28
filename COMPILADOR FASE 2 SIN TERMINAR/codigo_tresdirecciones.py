#codigo_tresdirecciones.py
class ThreeAddressCode:
    """Representa una instrucción de código de tres direcciones"""
    def __init__(self, op, arg1=None, arg2=None, result=None):
        self.op = op
        self.arg1 = arg1
        self.arg2 = arg2
        self.result = result

    def __str__(self):
        if self.op in ['=', 'ASSIGN']:
            return f"{self.result} = {self.arg1}"
        if self.op in ['+', '-', '*', '/', '%']:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        if self.op in ['==', '!=', '<', '>', '<=', '>=']:
            return f"{self.result} = {self.arg1} {self.op} {self.arg2}"
        if self.op == 'GOTO':
            return f"goto {self.result}"
        if self.op == 'IF_FALSE':
            return f"if_false {self.arg1} goto {self.result}"
        if self.op == 'IF_TRUE':
            return f"if_true {self.arg1} goto {self.result}"
        if self.op == 'LABEL':
            return f"{self.result}:"
        if self.op == 'CALL':
            return f"{self.result} = call {self.arg1}, {self.arg2}"
        if self.op == 'RETURN':
            return f"return {self.arg1}" if self.arg1 is not None else "return"
        if self.op == 'PARAM':
            return f"param {self.arg1}"
        if self.op == 'PRINT':
            return f"print {self.arg1}"
        return f"{self.op} {self.arg1} {self.arg2} {self.result}"

class IntermediateCodeGenerator:
    """Generador de código intermedio de tres direcciones"""
    def __init__(self):
        self.code = []
        self.temp_counter = 0
        self.label_counter = 0
        self.current_function = None

    def generate(self, ast_node):
        self.code.clear()
        self.temp_counter = 0
        self.label_counter = 0
        self._gen(ast_node)
        return self.code

    def _gen(self, node):
        if not node: return None
        name = type(node).__name__.lower()
        fn = getattr(self, f"_gen_{name}", None)
        return fn(node) if fn else None

    def _gen_program(self, node):
        for stmt in node.sentencias:
            self._gen(stmt)

    def _gen_funcdecl(self, node):
        prev = self.current_function
        self.current_function = node.name
        self.code.append(ThreeAddressCode('LABEL', result=f"func_{node.name}"))
        for stmt in node.body:
            self._gen(stmt)
        # asegurar return
        if not self.code or self.code[-1].op != 'RETURN':
            self.code.append(ThreeAddressCode('RETURN'))
        self.current_function = prev

    def _gen_vardecl(self, node):
        if node.expr:
            temp = self._gen(node.expr)
            self.code.append(ThreeAddressCode('ASSIGN', temp, None, node.nombre))

    def _gen_assign(self, node):
        val = self._gen(node.expr)
        if node.op == '=':
            self.code.append(ThreeAddressCode('ASSIGN', val, None, node.nombre))
        else:
            # x += y, etc.
            op = node.op[0]
            temp = self.new_temp()
            self.code.append(ThreeAddressCode(op, node.nombre, val, temp))
            self.code.append(ThreeAddressCode('ASSIGN', temp, None, node.nombre))

    def _gen_literal(self, node):
        return str(node.value)

    def _gen_varref(self, node):
        return node.nombre

    def _gen_binop(self, node):
        l = self._gen(node.left)
        r = self._gen(node.right)
        temp = self.new_temp()
        self.code.append(ThreeAddressCode(node.op, l, r, temp))
        return temp

    def _gen_compareop(self, node):
        return self._gen_binop(node)

    def _gen_logicalop(self, node):
        # para AND/OR simplificado en un binop
        return self._gen_binop(node) if node.right else None

    def _gen_print(self, node):
        val = self._gen(node.expr)
        self.code.append(ThreeAddressCode('PRINT', val))

    def _gen_return(self, node):
        if node.expr:
            val = self._gen(node.expr)
            self.code.append(ThreeAddressCode('RETURN', val))
        else:
            self.code.append(ThreeAddressCode('RETURN'))

    def _gen_funccall(self, node):
        for arg in node.args:
            a = self._gen(arg)
            self.code.append(ThreeAddressCode('PARAM', a))
        temp = self.new_temp()
        self.code.append(ThreeAddressCode('CALL', node.name, len(node.args), temp))
        return temp

    def _gen_ifthen(self, node):
        cond = self._gen(node.cond)
        end = self.new_label()
        self.code.append(ThreeAddressCode('IF_FALSE', cond, None, end))
        for s in node.then_body:
            self._gen(s)
        self.code.append(ThreeAddressCode('LABEL', result=end))

    def _gen_ifthenelse(self, node):
        cond = self._gen(node.cond)
        else_lbl = self.new_label(); end = self.new_label()
        self.code.append(ThreeAddressCode('IF_FALSE', cond, None, else_lbl))
        for s in node.then_body: self._gen(s)
        self.code.append(ThreeAddressCode('GOTO', result=end))
        self.code.append(ThreeAddressCode('LABEL', result=else_lbl))
        for s in node.else_body: self._gen(s)
        self.code.append(ThreeAddressCode('LABEL', result=end))

    def _gen_while(self, node):
        start = self.new_label(); end = self.new_label()
        self.code.append(ThreeAddressCode('LABEL', result=start))
        cond = self._gen(node.cond)
        self.code.append(ThreeAddressCode('IF_FALSE', cond, None, end))
        for s in node.body: self._gen(s)
        self.code.append(ThreeAddressCode('GOTO', result=start))
        self.code.append(ThreeAddressCode('LABEL', result=end))

    def new_temp(self):
        t = f"t{self.temp_counter}"
        self.temp_counter += 1
        return t

    def new_label(self):
        l = f"L{self.label_counter}"
        self.label_counter += 1
        return l

    def print_code(self):
        print("\n📋 CÓDIGO DE TRES DIRECCIONES:")
        for i, instr in enumerate(self.code):
            print(f"{i:3d}: {instr}")

    def get_code_as_string(self):
        return "\n".join(str(instr) for instr in self.code)
