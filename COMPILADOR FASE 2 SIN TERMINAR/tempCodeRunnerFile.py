from parser_module import analizar_sintaxis
from tkinter import Tk, filedialog


def seleccionar_archivo():
    """Función para seleccionar un archivo usando Tkinter."""
    Tk().withdraw()  # Ocultar la ventana principal de Tkinter
    archivo = filedialog.askopenfilename(
        title="Seleccionar archivo",
        filetypes=(("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*"))
    )
    return archivo

if __name__ == "__main__":
    
    
    ruta_archivo = seleccionar_archivo()
    if ruta_archivo:
        try:
            # Leer el contenido del archivo seleccionado
            with open(ruta_archivo, "r", encoding="utf-8") as archivo:
                contenido = archivo.read()
            print("Archivo leído correctamente.\n")
            
            # Pasar el contenido del archivo al parser para su análisis
            analizar_sintaxis(contenido)
        except FileNotFoundError:
            print("Error: No se encontró el archivo.")
        except Exception as e:
            print(f"Error inesperado: {e}")
    else:
        print("No se seleccionó ningún archivo.")