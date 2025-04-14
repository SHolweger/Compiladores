from lexer import lexer
from parser import analizar_sintaxis


def main():
    # Solicita el nombre del archivo fuente
    filename = input("\nIngresa el nombre del archivo fuente: ")

    try:
        with open(filename, 'r') as file:
            source_code = file.read()
    except FileNotFoundError:
        print(f"\n[Error] El archivo '{filename}' no fue encontrado.")
        return

    # Ejecuta el análisis sintáctico (internamente hace léxico también)
    analizar_sintaxis(filename)

    print("\nAnálisis completado. Reportes generados en la carpeta actual.")


if __name__ == '__main__':
    main()
