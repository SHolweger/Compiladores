import re

# Aqui se definen todos los Tokens
PALABRAS_CLAVE = {"inicio", "numero", "decimal", "si", "sino", "mientras", "repetir", "regresa"}
OPERADORES = {"+", "-", "*", "/", "%", "=", "==", "!=", ">", "<", ">=", "<="}
SEPARADORES = {";", ",", "(", ")", "{", "}"}
COMENTARIOS = r"//.*"

# Estas son las expresiones regulares para los tokens
TOKEN_PATTERNS = [
    (r"\b\d+\b", "NUMERO"), 
    (r"\b\d+\.\d+\b", "DECIMAL"),  
    (r"\".*?\"", "CADENA"), 
    (r"\b[a-zA-Z_]\w*\b", "IDENTIFICADOR"),
]

def leer_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            contenido = archivo.readlines()
        print("✅ Archivo leído correctamente.\n")
        return contenido
    except FileNotFoundError:
        print("❌ Error: No se encontró el archivo.")
        return []
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return []

def analizar_lexico(lineas):
    tokens = []
    errores = []

    for num_linea, linea in enumerate(lineas, start=1):
        linea = linea.strip()

        linea = re.sub(COMENTARIOS, "", linea)

        # Se definen los Tokens linea por linea
        palabras = re.findall(r"[a-zA-Z_]\w*|\d+\.\d+|\d+|[^\s]", linea)
        columna = 1

        for palabra in palabras:
            tipo = "ERROR"

            # Aqui se mira si la palabra es palabra clave
            if palabra in PALABRAS_CLAVE:
                tipo = "PALABRA_CLAVE"
            elif palabra in OPERADORES:
                tipo = "OPERADOR"
            elif palabra in SEPARADORES:
                tipo = "SEPARADOR"
            elif re.fullmatch(r"\b\d+\b", palabra):
                tipo = "NUMERO"
            elif re.fullmatch(r"\b\d+\.\d+\b", palabra):
                tipo = "DECIMAL"
            elif re.fullmatch(r"\".*?\"", palabra):
                tipo = "CADENA"
            elif re.fullmatch(r"\b[a-zA-Z_]\w*\b", palabra):
                tipo = "IDENTIFICADOR"
            else:
                errores.append((palabra, num_linea, columna))  # Errores

            tokens.append((palabra, tipo, num_linea, columna))
            columna += len(palabra) + 1  

    return tokens, errores

def generar_html(tokens, errores):
    with open("reporte_tokens.html", "w", encoding="utf-8") as archivo:
        archivo.write("<html><head><title>TABLA DE TOKENS</title></head><body>")
        archivo.write("<h1>TABLA DE TOKENS</h1>")
        archivo.write("<table border='1'><tr><th>Token</th><th>Tipo</th><th>Línea</th><th>Columna</th></tr>")

        for token in tokens:
            palabra, tipo, linea, columna = token
            color = "black" if tipo != "ERROR" else "red"
            archivo.write(f"<tr style='color:{color};'><td>{palabra}</td><td>{tipo}</td><td>{linea}</td><td>{columna}</td></tr>")

        archivo.write("</table>")

        if errores:
            archivo.write("<h2>Errores Léxicos</h2>")
            archivo.write("<ul>")
            for error in errores:
                palabra, linea, columna = error
                archivo.write(f"<li style='color:red;'>Error: '{palabra}' en línea {linea}, columna {columna}</li>")
            archivo.write("</ul>")

        archivo.write("</body></html>")

#Archivoo
ruta_archivo = "codigo_fuente.txt"  

lineas = leer_archivo(ruta_archivo)

# Aqui esta el Analizador Lexico
if lineas:
    print("\n -----Contenido leído------\n")
    for i, linea in enumerate(lineas, start=1):
        print(f"{i}: {linea.strip()}")

    tokens_encontrados, errores_lexicos = analizar_lexico(lineas)

    print("\n---------Tokens encontrados-------\n")
    for token in tokens_encontrados:
        print(token)

    # Aqui se crear el HTML con la tabla de Tokens, esta en la ruta del archivo donde se guarde el proyecto
    generar_html(tokens_encontrados, errores_lexicos)
    print("\n✅ Reporte generado: reporte_tokens.html en la ruta del archivo")


