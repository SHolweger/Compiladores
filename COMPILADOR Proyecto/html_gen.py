import os
import webbrowser

def abrir_html(nombre_archivo):
    path = os.path.abspath(nombre_archivo)
    webbrowser.open(f'file://{path}')

def generar_html_tokens(tokens, nombre_archivo="tokens.html"):
    html = """
    <html><head><title>Bitácora de Tokens</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; text-align: center; }
        table { width: 80%; margin: auto; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ccc; padding: 10px; }
        th { background: #4CAF50; color: white; }
    </style></head><body>
    <h2>Bitácora de Tokens</h2><table><tr><th>Token</th><th>Valor</th><th>Línea</th></tr>
    """
    for token in tokens:
        html += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{token.lineno}</td></tr>"
    html += "</table></body></html>"

def generar_html_errores(errores, nombre_archivo="errores.html"):
    html = """
    <html><head><title>Bitácora de Errores</title>
    <style>
        body { font-family: Arial; background: #fff4f4; text-align: center; }
        table { width: 80%; margin: auto; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ccc; padding: 10px; }
        th { background: #d9534f; color: white; }
    </style></head><body>
    <h2>Bitácora de Errores</h2><table><tr><th>Mensaje</th><th>Línea</th></tr>
    """
    for error, linea in errores:
        html += f"<tr><td>{error}</td><td>{linea}</td></tr>"
    html += "</table></body></html>"

def generar_html_tabla_simbolos(tabla_simbolos, nombre_archivo="tabla_simbolos.html"):
    html = """
    <html><head><title>Tabla de Simbolos</title>
    <style>
        body { font-family: Arial; background: #eef; text-align: center; }
        table { width: 60%; margin: auto; border-collapse: collapse; background: white; }
        th, td { border: 1px solid #ccc; padding: 10px; }
        th { background: #337ab7; color: white; }
    </style></head><body>
    <h2>Tabla de Simbolos</h2><table><tr><th>Nombre</th><th>Tipo</th><th>Valor</th></tr>
    """
    for nombre, datos in tabla_simbolos.items():
        html += f"<tr><td>{nombre}</td><td>{datos['tipo']}</td><td>{datos['valor']}</td></tr>"
    html += "</table></body></html>"

def abrir_todos_los_html():
    abrir_html("tokens.html")
    abrir_html("errores.html")
    abrir_html("tabla_simbolos.html")
