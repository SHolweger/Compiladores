import tkinter as tk
from tkinter import filedialog
import html_gen
import tabla_simbolos
from lexer import construir_lexer, analizar_codigo
from parser import analizar_sintaxis

def seleccionar_archivo():
    """Abre una ventana gráfica para seleccionar el archivo fuente."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(
        title="Selecciona el archivo fuente",
        filetypes=[("Archivos de texto", "*.txt *.src"), ("Todos los archivos", "*.*")]
    )

def generar_reportes(tokens, errores_lexicos, errores_sintacticos):
    html_gen.generar_pagina_inicio()
    html_gen.generar_html_tokens(tokens)
    html_gen.generar_html_errores(errores_lexicos, "errores_lexicos.html", "lexico")
    html_gen.generar_html_errores(errores_sintacticos, "errores_sintacticos.html", "sintactico")
    html_gen.generar_html_errores(tabla_simbolos.errores_semanticos, "errores_semanticos.html", "semantico")
    html_gen.generar_html_tabla_simbolos(tabla_simbolos.tabla)
    html_gen.abrir_todos_los_html()

def main():
    ruta_archivo = seleccionar_archivo()

    if not ruta_archivo:
        print("No se seleccionó ningún archivo.")
        return

    try:
        with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
            codigo = archivo.read()

        print("\nCódigo leído desde el archivo:")
        print("----------------------------------")
        print(codigo)

        # Construir lexer y realizar análisis léxico
        lexer = construir_lexer()
        tokens, errores_lexicos = analizar_codigo(codigo, lexer)

        print("\nTokens extraídos:")
        for tok in tokens:
            col = getattr(tok, "column", "¿?")
            print(f"{tok.type} -> {tok.value} (Línea {tok.lineno}, Columna {col})")

        print("\nErrores léxicos:")
        if errores_lexicos:
            for err, linea, columna in errores_lexicos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("No se encontraron errores léxicos.")

        # Análisis sintáctico
        errores_sintacticos = analizar_sintaxis(codigo)

        print("\nErrores sintácticos:")
        if errores_sintacticos:
            for err, linea, columna in errores_sintacticos:
                print(f"{err} en Línea {linea}, Columna {columna}")
        else:
            print("No se encontraron errores sintácticos.")

        # Generar reportes HTML
        generar_reportes(tokens, errores_lexicos, errores_sintacticos)

        print("\n✅ Reportes generados correctamente. Puedes abrir los HTML en tu navegador.")

    except FileNotFoundError:
        print("❌ No se pudo abrir el archivo. Verifica la ruta.")
    except Exception as e:
        print(f"❌ Error al procesar el archivo: {e}")

if __name__ == "__main__":
    main()
