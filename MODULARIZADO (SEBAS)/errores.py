# errores.py

# Listas globales de errores
errores_lexicos = []
errores_sintacticos = []
errores_semanticos = []

def registrar_error(lista, mensaje, linea, columna=0):
    """Agrega un error a la lista correspondiente."""
    lista.append((mensaje, linea, columna))

def limpiar_errores():
    """Limpia todas las listas de errores."""
    errores_lexicos.clear()
    errores_sintacticos.clear()
    errores_semanticos.clear()

def hay_errores():
    """Devuelve True si hay errores registrados en cualquiera de las listas."""
    return any([errores_lexicos, errores_sintacticos, errores_semanticos])

def todos_los_errores():
    """Devuelve una lista combinada de todos los errores."""
    return errores_lexicos + errores_sintacticos + errores_semanticos

def imprimir_errores():
    """Imprime todos los errores de manera formateada."""
    for tipo, lista in [("Léxicos", errores_lexicos), 
                        ("Sintácticos", errores_sintacticos), 
                        ("Semánticos", errores_semanticos)]:
        if lista:
            print(f"\nErrores {tipo}:")
            for mensaje, linea, columna in lista:
                print(f"  Línea {linea}, Columna {columna}: {mensaje}")
