import tkinter as tk
from tkinter import filedialog
import html_gen
import tabla_simbolos
import lexer
import parser
from errores import limpiar_errores

def seleccionar_archivo():
    """Abre una ventana gráfica para seleccionar el archivo fuente."""
    root = tk.Tk()
    root.withdraw()  # Oculta la ventana principal
    archivo = filedialog.askopenfilename(
        title="Selecciona el archivo fuente",
        filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
    )
    return archivo

def generar_reportes(tokens, errores_lexicos, errores_sintacticos):
    """Genera los reportes HTML de los errores y la tabla de símbolos."""
    html_gen.generar_pagina_inicio()
    
    if tokens:
        html_gen.generar_html_tokens(tokens)
    
    if errores_lexicos:
        html_gen.generar_html_errores(errores_lexicos, "errores_lexicos.html", "lexico")
    
    if errores_sintacticos:
        html_gen.generar_html_errores(errores_sintacticos, "errores_sintacticos.html", "sintactico")
    
    if tabla_simbolos.errores_semanticos:
        html_gen.generar_html_errores(tabla_simbolos.errores_semanticos, "errores_semanticos.html", "semantico")
    
    if tabla_simbolos.tabla_simbolos:
        html_gen.generar_html_tabla_simbolos(tabla_simbolos.tabla_simbolos)
    
    html_gen.abrir_todos_los_html()

def main():
    print("===== ANALIZADOR LEXICO, SINTACTICO Y SEMANTICO =====\n")

    ruta_archivo = seleccionar_archivo()

    if not ruta_archivo:
        print("No se seleccionó ningún archivo.")
        return

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()

        if not codigo.strip():
            print("El archivo está vacío.")
            return

        print("\nCódigo leído desde el archivo:")
        print("----------------------------------")
        print(codigo)

        # Limpiar los errores previos
        limpiar_errores()
        
        # Analizar código léxicamente
        print("\nAnálisis Léxico:")
        tokens, errores_lexicos = lexer.analizar_codigo(codigo, lexer)  # Usamos directamente el lexer

        if tokens:
            for tok in tokens:
                col = getattr(tok, "column", "¿?")
                print(f"{tok.type} -> {tok.value} (Linea {tok.lineno}, Columna {col})")

        if errores_lexicos:
            print("\nErrores Léxicos:")
            for err, linea, columna in errores_lexicos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("Sin errores léxicos.")

        # Analizar código sintácticamente
        print("\nAnálisis Sintáctico:")
        errores_sintacticos = parser.analizar_sintaxis(codigo)  # Asegúrate que esto retorne errores correctamente

        if errores_sintacticos:
            print("\nErrores Sintácticos:")
            for err, linea, columna in errores_sintacticos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("Sin errores sintácticos.")

        # Mostrar errores semánticos
        if tabla_simbolos.errores_semanticos:
            print("\nErrores Semánticos:")
            for err, linea, columna in tabla_simbolos.errores_semanticos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("Sin errores semánticos.")

        # Generar reportes HTML
        generar_reportes(tokens, errores_lexicos, errores_sintacticos)

        print("\nReportes generados correctamente. Puedes abrir los HTML en tu navegador.")

    except FileNotFoundError:
        print("No se pudo abrir el archivo. Verifica la ruta.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()
# MODULARIZADO SEBAS
# Este código es un analizador léxico, sintáctico y semántico modularizado.