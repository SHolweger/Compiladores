import os
import webbrowser
import time

def abrir_html(nombre_archivo):
    path = os.path.abspath(nombre_archivo)
    webbrowser.open(f'file://{path}')
    time.sleep(1)

def generar_menu():
    return """
    <div class='menu'>
        <a href='index.html'>Inicio</a>
        <a href='tokens.html'>Tokens</a>
        <a href='errores.html'>Errores</a>
        <a href='tabla_simbolos.html'>Tabla de Símbolos</a>
        <button onclick='window.scrollTo(0,0)'>⬆ Inicio</button>
        <button onclick='window.print()'>📄 Exportar PDF</button>
    </div>
    <style>
        .menu {
            text-align: center;
            margin: 20px;
            animation: slide-in 0.8s ease-in-out;
            background: #333;
            border-radius: 10px;
            padding: 20px;
        }
        .menu a, .menu button {
            margin: 0 10px;
            padding: 10px 20px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s ease, transform 0.3s ease;
        }
        .menu a:hover, .menu button:hover {
            background: #45a049;
            cursor: pointer;
            transform: scale(1.1);
        }
        @keyframes slide-in {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    </style>
    """

def generar_html_tokens(tokens, nombre_archivo="tokens.html"):
    html = f"""
    <html><head><title>Bitácora de Tokens</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #f9fafb; color: #333; }}
        h2 {{ color: #2c3e50; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 90%; margin: 30px auto; border-collapse: collapse; box-shadow: 0 0 10px rgba(0,0,0,0.1); animation: fadeInUp 1.2s ease-out; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #4CAF50; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        tr:hover {{ background-color: #e9ffe8; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Bitácora de Tokens</h2><table><tr><th>Token</th><th>Valor</th><th>Línea</th></tr>
    """
    for token in tokens:
        html += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{token.lineno}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
    abrir_html(nombre_archivo)

def generar_html_errores(errores, nombre_archivo="errores.html"):
    html = f"""
    <html><head><title>Bitácora de Errores</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #fff4f4; color: #333; }}
        h2 {{ color: #a00; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 90%; margin: 30px auto; border-collapse: collapse; box-shadow: 0 0 10px rgba(0,0,0,0.1); animation: fadeInUp 1.2s ease-out; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: center; }}
        th {{ background-color: #d9534f; color: white; }}
        tr:nth-child(even) {{ background-color: #fdf2f2; }}
        tr:hover {{ background-color: #f8d7da; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Bitácora de Errores</h2><table><tr><th>Mensaje</th><th>Línea</th></tr>
    """
    for error, linea in errores:
        html += f"<tr><td>{error}</td><td>{linea}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
    abrir_html(nombre_archivo)

def generar_html_tabla_simbolos(tabla_simbolos, nombre_archivo="tabla_simbolos.html"):
    html = f"""
    <html><head><title>Tabla de Símbolos</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: #eef2f7; color: #333; }}
        h2 {{ color: #2c3e50; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 70%; margin: 30px auto; border-collapse: collapse; box-shadow: 0 0 10px rgba(0,0,0,0.1); animation: fadeInUp 1.2s ease-out; }}
        th, td {{ border: 1px solid #ccc; padding: 12px; text-align: center; }}
        th {{ background-color: #337ab7; color: white; }}
        tr:nth-child(even) {{ background-color: #f2f9ff; }}
        tr:hover {{ background-color: #d9ecff; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(20px); }} to {{ opacity: 1; transform: translateY(0); }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Tabla de Símbolos</h2><table><tr><th>Nombre</th><th>Tipo</th><th>Valor</th></tr>
    """
    for nombre, datos in tabla_simbolos.items():
        html += f"<tr><td>{nombre}</td><td>{datos['tipo']}</td><td>{datos['valor']}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
    abrir_html(nombre_archivo)

def generar_pagina_inicio(nombre_archivo="index.html"):
    html = """
    <html><head><title>Inicio - Reportes del Compilador</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #6a11cb, #2575fc); text-align: center; color: white; animation: fadeIn 1s ease-in; }
        h1 { color: #fdfdfd; margin-top: 50px; font-size: 40px; }
        .btn-container { margin-top: 40px; animation: fadeInUp 1s ease-out; }
        a.btn {
            display: inline-block; margin: 10px; padding: 15px 30px;
            background-color: #007BFF; color: white; text-decoration: none;
            border-radius: 6px; font-size: 16px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        a.btn:hover { background-color: #0056b3; transform: scale(1.1); }
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
        @keyframes fadeInUp { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
    </style></head><body>
    <h1>Bienvenido al Reporte del Compilador</h1>
    <p>Selecciona una de las opciones para visualizar:</p>
    <div class='btn-container'>
        <a href='tokens.html' class='btn'>📄 Ver Tokens</a>
        <a href='errores.html' class='btn'>🚫 Ver Errores</a>
        <a href='tabla_simbolos.html' class='btn'>📘 Ver Tabla de Símbolos</a>
    </div>
    </body></html>
    """
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
    abrir_html(nombre_archivo)

def abrir_todos_los_html():
    abrir_html("index.html")
    abrir_html("tokens.html")
    abrir_html("errores.html")
    abrir_html("tabla_simbolos.html")