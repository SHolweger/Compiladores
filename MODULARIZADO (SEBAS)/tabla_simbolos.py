# tabla_simbolos.py

tabla_simbolos = {}
errores_sintacticos = []
errores_semanticos = []

# Para manejar el alcance de las variables
alcance_actual = 'global'  # Puede ser 'global' o el nombre de una función

def establecer_alcance(nuevo_alcance):
    global alcance_actual
    alcance_actual = nuevo_alcance

def agregar_simbolo(nombre, tipo, valor, linea, columna=0):
    if nombre not in tabla_simbolos:
        if verificar_tipo_valor(tipo, valor):
            tabla_simbolos[nombre] = {
                "tipo": tipo,
                "valor": valor,
                "linea": linea,
                "columna": columna,
                "alcance": alcance_actual
            }
        else:
            errores_semanticos.append((
                f"Error semántico: El valor '{valor}' no es compatible con el tipo '{tipo}'",
                linea,
                columna
            ))
    else:
        errores_semanticos.append((
            f"Error semántico: Variable '{nombre}' ya ha sido declarada",
            linea,
            columna
        ))

def actualizar_simbolo(nombre, nuevo_valor, linea, columna=0):
    if nombre in tabla_simbolos:
        tipo = tabla_simbolos[nombre]["tipo"]
        if verificar_tipo_valor(tipo, nuevo_valor):
            tabla_simbolos[nombre]["valor"] = nuevo_valor
        else:
            errores_semanticos.append((
                f"Error semántico: Tipo incompatible al asignar valor a '{nombre}'",
                linea,
                columna
            ))
    else:
        errores_semanticos.append((
            f"Error semántico: Variable '{nombre}' no ha sido declarada",
            linea,
            columna
        ))

def verificar_simbolo(nombre, linea, columna=0):
    if nombre not in tabla_simbolos:
        errores_semanticos.append((
            f"Error semántico: Variable '{nombre}' no ha sido declarada",
            linea,
            columna
        ))
        return False
    return True

def verificar_variable_no_inicializada(nombre, linea, columna=0):
    if nombre in tabla_simbolos and tabla_simbolos[nombre]["valor"] is None:
        errores_semanticos.append((
            f"Error semántico: Variable '{nombre}' utilizada antes de ser inicializada",
            linea,
            columna
        ))

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
