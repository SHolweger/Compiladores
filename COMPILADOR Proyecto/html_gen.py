#Generador de reportes HTML
import os

def generar_html_tokens(tokens, nombre_archivo="tokens.html"):
    html = """
    <html>
    <head>
        <title>Bitácora de Tokens</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #f4f4f4; text-align: center; }
            h2 { color: #333; }
            table { width: 80%; margin: auto; border-collapse: collapse; background: white; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #4CAF50; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Bitácora de Tokens</h2>
        <table>
            <tr>
                <th>Token</th>
                <th>Valor</th>
                <th>Línea</th>
            </tr>
    """
    
    for token in tokens:
        html += f"""
        <tr>
            <td>{token.type}</td>
            <td>{token.value}</td>
            <td>{token.lineno}</td>
        </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def generar_html_errores(errores, nombre_archivo="errores.html"):
    html = """
    <html>
    <head>
        <title>Bitácora de Errores</title>
        <style>
            body { font-family: Arial, sans-serif; background-color: #ffdddd; text-align: center; }
            h2 { color: #a00; }
            table { width: 80%; margin: auto; border-collapse: collapse; background: white; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: center; }
            th { background-color: #d9534f; color: white; }
            tr:nth-child(even) { background-color: #f2f2f2; }
        </style>
    </head>
    <body>
        <h2>Bitácora de Errores</h2>
        <table>
            <tr>
                <th>Error</th>
                <th>Línea</th>
            </tr>
    """
    
    for error in errores:
        html += f"""
        <tr>
            <td>{error[0]}</td>
            <td>{error[1]}</td>
        </tr>
        """
    
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def generar_html_tabla_simbolos(tabla_simbolos):
    html = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tabla de Símbolos</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    <h2>Tabla de Símbolos</h2>
    <table border="1">
        <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Valor</th>
        </tr>"""
    
    for nombre, datos in tabla_simbolos.items():
        html += f"""
        <tr>
            <td>{nombre}</td>
            <td>{datos['tipo']}</td>
            <td>{datos['valor']}</td>
        </tr>"""
    
    html += """
    </table>
</body>
</html>"""
    
    with open("tabla_simbolos.html", "w", encoding="utf-8") as file:
        file.write(html)
    print("Tabla de símbolos generada: tabla_simbolos.html")

if __name__ == "__main__":
    print("Este módulo genera reportes HTML de tokens y errores.")
