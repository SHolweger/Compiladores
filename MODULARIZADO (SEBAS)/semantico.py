# semantico.py

from errores import registrar_error, errores_semanticos

def tipo_valido(tipo, valor):
    """Verifica que el valor coincida con el tipo declarado."""
    if tipo == "NUMERO":
        return isinstance(valor, int)
    elif tipo == "DECIMAL":
        return isinstance(valor, float)
    elif tipo == "BOOLEANO":
        return isinstance(valor, bool)
    elif tipo == "CADENA":
        return isinstance(valor, str)
    return False

def evaluar_expresion(op1, operador, op2, linea, columna=0):
    """Evalúa expresiones aritméticas, lógicas y de comparación."""
    try:
        if operador == '+':
            return op1 + op2
        elif operador == '-':
            return op1 - op2
        elif operador == '*':
            return op1 * op2
        elif operador == '/':
            if op2 == 0:
                raise ZeroDivisionError
            return op1 / op2
        elif operador == '>':
            return op1 > op2
        elif operador == '<':
            return op1 < op2
        elif operador == '==':
            return op1 == op2
        elif operador == '!=':
            return op1 != op2
        elif operador == '&&':
            if isinstance(op1, bool) and isinstance(op2, bool):
                return op1 and op2
            else:
                raise TypeError("El operador '&&' requiere operandos booleanos")
        elif operador == '||':
            if isinstance(op1, bool) and isinstance(op2, bool):
                return op1 or op2
            else:
                raise TypeError("El operador '||' requiere operandos booleanos")
        else:
            raise ValueError(f"Operador desconocido: {operador}")
    except ZeroDivisionError:
        registrar_error(errores_semanticos, "Error semántico: División por cero.", linea, columna)
        return 0
    except Exception as e:
        registrar_error(errores_semanticos, f"Error semántico: {str(e)}", linea, columna)
        return 0
