# tabla_simbolos.py

from errores import registrar_error, errores_semanticos

tabla_simbolos = {}
alcance_actual = 'global'  # Puede ser 'global' o el nombre de una función

# ---------------------
# Manejo de Alcance
# ---------------------
def establecer_alcance(nuevo_alcance):
    global alcance_actual
    alcance_actual = nuevo_alcance

# ---------------------
# Manipulación de Símbolos
# ---------------------
def agregar_simbolo(nombre, tipo, valor, linea, columna=0):
    clave = (nombre, alcance_actual)
    if clave not in tabla_simbolos:
        if verificar_tipo_valor(tipo, valor):
            tabla_simbolos[clave] = {
                "tipo": tipo,
                "valor": valor,
                "linea": linea,
                "columna": columna,
                "alcance": alcance_actual
            }
        else:
            registrar_error(errores_semanticos,
                f"Error semántico: El valor '{valor}' no es compatible con el tipo '{tipo}'",
                linea, columna)
    else:
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{nombre}' ya ha sido declarada en el alcance '{alcance_actual}'",
            linea, columna)

def actualizar_simbolo(nombre, nuevo_valor, linea=0, columna=0):
    simbolo = obtener_simbolo(nombre)
    if simbolo:
        tipo = simbolo["tipo"]
        if verificar_tipo_valor(tipo, nuevo_valor):
            simbolo["valor"] = nuevo_valor
        else:
            registrar_error(errores_semanticos,
                f"Error semántico: Tipo incompatible al asignar valor a '{nombre}'",
                linea, columna)
    else:
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{nombre}' no ha sido declarada",
            linea, columna)

def obtener_simbolo(nombre):
    clave = (nombre, alcance_actual)
    if clave in tabla_simbolos:
        return tabla_simbolos[clave]
    
    # Buscar en global si no se encontró en alcance local
    clave_global = (nombre, 'global')
    return tabla_simbolos.get(clave_global)

# ---------------------
# Verificaciones Semánticas
# ---------------------
def verificar_simbolo(nombre, linea=0, columna=0):
    if not obtener_simbolo(nombre):
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{nombre}' no ha sido declarada",
            linea, columna)
        return False
    return True

def verificar_variable_no_inicializada(nombre, linea=0, columna=0):
    simbolo = obtener_simbolo(nombre)
    if simbolo and simbolo["valor"] is None:
        registrar_error(errores_semanticos,
            f"Error semántico: Variable '{nombre}' utilizada antes de ser inicializada",
            linea, columna)

# ---------------------
# Validación de Tipos
# ---------------------
def verificar_tipo_valor(tipo, valor):
    if tipo == "NUMERO":
        return isinstance(valor, int)
    elif tipo == "DECIMAL":
        return isinstance(valor, float)
    elif tipo == "BOOLEANO":
        return isinstance(valor, bool)
    elif tipo == "CADENA":
        return isinstance(valor, str)
    return False
