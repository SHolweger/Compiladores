#main.py
from parser_module import analizar_sintaxis
from codigo_tresdirecciones import IntermediateCodeGenerator
from optimizador_codegen import Optimizer, CCodeGenerator
from tkinter import Tk, filedialog
import html_gen            # ← Import global, fuera de cualquier función o bloque

def seleccionar_archivo():
    """Función para seleccionar un archivo usando Tkinter."""
    Tk().withdraw()
    return filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )

def main():
    ruta_archivo = seleccionar_archivo()
    if not ruta_archivo:
        print("No se seleccionó ningún archivo.")
        return

    try:
        # 1) Leer el archivo
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            contenido = f.read()
        print("Archivo leído correctamente.\n")

        # 2) Análisis léxico/sintáctico/semántico (genera HTML)
        ast = analizar_sintaxis(contenido)
        if ast is None:
            print("No se produjo AST; revisa errores en el HTML de errores.")
            return

        # 3) Generar TAC
        tac_gen = IntermediateCodeGenerator()
        tac = tac_gen.generate(ast)
        tac_gen.print_code()
        with open("codigo_intermedio.txt", "w", encoding="utf-8") as f:
            f.write(tac_gen.get_code_as_string())

        # 4) Optimizar TAC
        optimizer = Optimizer(tac)
        tac_opt = optimizer.optimize()
        with open("codigo_intermedio_opt.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(str(instr) for instr in tac_opt))

        # 5) Generar C
        cgen = CCodeGenerator(tac_opt)
        c_code = cgen.generate()
        with open("programa.c", "w", encoding="utf-8") as f:
            f.write(c_code)
        print("Código C generado en programa.c")

        # 6) Abrir página de reportes
        html_gen.abrir_html("index.html")

    except FileNotFoundError:
        print("Error: No se encontró el archivo.")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()