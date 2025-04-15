#main.py
import tkinter as tk
from tkinter import filedialog
import html_gen
import tabla_simbolos
import lexer
import parser

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
    html_gen.generar_pagina_inicio()
    html_gen.generar_html_tokens(tokens)
    html_gen.generar_html_errores(errores_lexicos, "errores_lexicos.html", "lexico")
    html_gen.generar_html_errores(errores_sintacticos, "errores_sintacticos.html", "sintactico")
    html_gen.generar_html_errores(tabla_simbolos.errores_semanticos, "errores_semanticos.html", "semantico")
    html_gen.generar_html_tabla_simbolos(tabla_simbolos.tabla_simbolos)
    html_gen.abrir_todos_los_html()

def main():
    print("===== ANALIZADOR LEXICO, SINTACTICO Y SEMANTICO =====\n")

    ruta_archivo = seleccionar_archivo()

    if not ruta_archivo:
        print("No se selecciono ningún archivo.")
        return

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()

        if not codigo.strip():
            print("El archivo está vacío.")
            return

        print("\nCodigo leido desde el archivo:")
        print("----------------------------------")
        print(codigo)

        # Analizar código léxicamente
        print("\nAnalisis Lexico:")
        lexer_instance = lexer.construir_lexer()  # Creando una instancia del lexer
        tokens, errores_lexicos = lexer.analizar_codigo(codigo, lexer_instance)

        for tok in tokens:
            col = getattr(tok, "column", "¿?")
            print(f"{tok.type} -> {tok.value} (Linea {tok.lineno}, Columna {col})\n")

        if errores_lexicos:
            print("\nErrores Lexicos:")
            for err, linea, columna in errores_lexicos:
                print(f"{err} en Linea {linea}, Columna {columna}")
        else:
            print("Sin errores lexicos.")

        # Analizar código sintácticamente
        print("\nAnalisis Sintactico:")
        errores_sintacticos = parser.analizar_sintaxis(codigo)

        if errores_sintacticos:
            print("\nErrores Sintacticos:")
            for err, linea, columna in errores_sintacticos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("Sin errores sintacticos.")

        # Mostrar errores semánticos
        if tabla_simbolos.errores_semanticos:
            print("\nErrores Semanticos:")
            for err, linea, columna in tabla_simbolos.errores_semanticos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("Sin errores semanticos.")

        # Generar reportes HTML
        generar_reportes(tokens, errores_lexicos, errores_sintacticos)

        print("\nReportes generados correctamente. Puedes abrir los HTML en tu navegador.")

    except FileNotFoundError:
        print("No se pudo abrir el archivo. Verifica la ruta.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()