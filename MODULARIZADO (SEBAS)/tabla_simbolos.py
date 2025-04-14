# tabla_simbolos.py

tabla_simbolos = {}
errores_sintacticos = []

def agregar_simbolo(nombre, tipo, valor, linea):
    tipo = tipo.lower()
    if nombre in tabla_simbolos:
        errores_sintacticos.append((f"Error: La variable '{nombre}' ya ha sido declarada.", linea))
    else:
        tabla_simbolos[nombre] = {'tipo': tipo, 'valor': valor}

def actualizar_simbolo(nombre, valor, linea):
    if nombre in tabla_simbolos:
        tipo = tabla_simbolos[nombre]['tipo']
        if tipo == 'numero' and isinstance(valor, int):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'decimal' and isinstance(valor, float):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'booleano' and isinstance(valor, bool):
            tabla_simbolos[nombre]['valor'] = valor
        elif tipo == 'cadena' and isinstance(valor, str):  
            tabla_simbolos[nombre]['valor'] = valor
        else:
            errores_sintacticos.append((f"Tipo de dato incorrecto para la variable '{nombre}'", linea))
    else:
        errores_sintacticos.append((f"La variable '{nombre}' no ha sido declarada.", linea))

def verificar_simbolo(nombre, linea):
    if nombre not in tabla_simbolos:
        errores_sintacticos.append((f"La variable '{nombre}' no ha sido declarada.", linea))
        return False
    return True
