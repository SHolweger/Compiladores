#optimizador_codegen.py
from codigo_tresdirecciones import ThreeAddressCode

class Optimizer:
    """Optimización de TAC: plegado de constantes y eliminación de código muerto."""
    def __init__(self, code):
        self.code = code

    def constant_folding(self):
        folded = []
        for instr in self.code:
            if instr.op in ['+', '-', '*', '/', '%', '==', '!=', '<', '>', '<=', '>=']:
                try:
                    a1 = int(instr.arg1) if instr.arg1.isdigit() else float(instr.arg1)
                    a2 = int(instr.arg2) if instr.arg2.isdigit() else float(instr.arg2)
                    res = eval(f"{a1}{instr.op}{a2}")
                    folded.append(ThreeAddressCode('ASSIGN', str(res), None, instr.result))
                    continue
                except:
                    pass
            folded.append(instr)
        self.code = folded
        return self

    def dead_code_elim(self):
        used = set()
        for instr in self.code:
            if instr.arg1 and instr.arg1.startswith('t'):
                used.add(instr.arg1)
            if instr.arg2 and instr.arg2.startswith('t'):
                used.add(instr.arg2)
        optimized = []
        for instr in reversed(self.code):
            if isinstance(instr.result, str) and instr.result.startswith('t') and instr.result not in used:
                continue
            optimized.insert(0, instr)
        self.code = optimized
        return self

    def optimize(self):
        return self.constant_folding().dead_code_elim().code

class CCodeGenerator:
    """Genera código C desde TAC optimizado."""
    def __init__(self, tac_list):
        self.tac = tac_list

    def generate(self):
        lines = ["#include <stdio.h>\n"]
        temps = {instr.result for instr in self.tac if instr.result and instr.result.startswith('t')}
        if temps:
            decl = ", ".join(sorted(temps))
            lines.append(f"int {decl};\n")
        for instr in self.tac:
            if instr.op == 'ASSIGN':
                lines.append(f"{instr.result} = {instr.arg1};")
            elif instr.op in ['+', '-', '*', '/', '%']:
                lines.append(f"{instr.result} = {instr.arg1} {instr.op} {instr.arg2};")
            elif instr.op == 'PRINT':
                lines.append(f'printf("%d\\n", {instr.arg1});')
            elif instr.op == 'RETURN':
                if instr.arg1:
                    lines.append(f"return {instr.arg1};")
                else:
                    lines.append("return;")
            # GOTO, IF_FALSE, LABEL, etc. puedes ampliar aquí si lo necesitas
        return "\n".join(lines)
