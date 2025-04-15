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
        <a href='index.html'>🏠 Inicio</a>
        <a href='tokens.html'>📄 Tokens</a>
        <a href='errores.html'>❌ Errores</a>
        <a href='tabla_simbolos.html'>📘 Tabla de Simbolos</a>
        <button onclick='window.print()'>🖨️ Exportar PDF</button>
    </div>
    <style>
        .menu {
            background-color: #333;
            overflow: hidden;
            text-align: center;
            padding: 10px;
        }
        .menu a, .menu button {
            display: inline-block;
            color: white;
            padding: 10px 20px;
            text-decoration: none;
            margin: 0 10px;
            background-color: #444;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        .menu a:hover, .menu button:hover {
            background-color: #666;
        }
        .scroll-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #00c853;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 50%;
            font-size: 20px;
            cursor: pointer;
        }
    </style>
    <button class='scroll-top' onclick='window.scrollTo({top: 0, behavior: "smooth"})'>⬆</button>
    """

def generar_html_tokens(tokens, nombre_archivo="tokens.html"):
    html = f"""
    <html><head><title>Bitacora de Tokens</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/3135/3135715.png" type="image/png">
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #00c853, #43cea2); color: white; }}
        h2 {{ color: white; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 90%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }}
        th, td {{ border: 1px solid #2e7d32; padding: 12px; text-align: center; }}
        th {{ background-color: #2e7d32; color: white; }}
        tr:nth-child(even) {{ background-color: #f0f0f0; }}
        tr:hover {{ background-color: #dcedc8; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Bitacora de Tokens</h2><table><tr><th>Token</th><th>Valor</th><th>Linea</th><th>Columna</th></tr>
    """
    
    for token in tokens:
        html += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{token.lineno}</td><td>{token.columna}</td></tr>"
    
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def generar_html_errores(errores, nombre_archivo="errores.html", tipo="lexico"):
    html = f"""
    <html><head><title>Errores {tipo.capitalize()}</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/1828/1828843.png" type="image/png">
    <style>
        body {{ font-family: sans-serif; }}
        h2 {{ text-align: center; animation: fadeIn 0.8s; }}
        table {{ width: 80%; margin: auto; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #a00; color: #fff; }}
        tr:nth-child(even) {{ background-color: #fdd; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Bitacora de Errores {tipo.capitalize()}</h2>
    <table>
        <tr><th>Descripcion</th><th>Linea</th><th>Columna</th></tr>
    """
    for descripcion, linea, columna in errores:
        html += f"<tr><td>{descripcion}</td><td>{linea}</td><td>{columna}</td></tr>"

    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def generar_html_tabla_simbolos(tabla_simbolos, nombre_archivo="tabla_simbolos.html"):
    html = f"""
    <html><head><title>Tabla de Simbolos</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/2917/2917997.png" type="image/png">
    <style>
        body {{ font-family: sans-serif; }}
        h2 {{ text-align: center; animation: fadeIn 0.8s; }}
        table {{ width: 80%; margin: auto; border-collapse: collapse; }}
        th, td {{ border: 1px solid #ccc; padding: 8px; text-align: center; }}
        th {{ background-color: #004488; color: #fff; }}
        tr:nth-child(even) {{ background-color: #eef; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Tabla de Simbolos</h2>
    <table>
        <tr><th>Nombre</th><th>Tipo</th><th>Valor</th></tr>
    """
    for nombre, datos in tabla_simbolos.items():
        html += f"<tr><td>{nombre}</td><td>{datos['tipo']}</td><td>{datos['valor']}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def generar_pagina_inicio(nombre_archivo="index.html"):
    html = """
    <html><head><title>Inicio - Reportes del Compilador</title>
    <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/857/857681.png" type="image/png">
    <style>
        body { text-align: center; font-family: sans-serif; background-color: #f2f2f2; padding-top: 40px; }
        .btn-container { margin-top: 30px; }
        .btn {
            display: inline-block; padding: 10px 20px; margin: 10px;
            background-color: #333; color: #fff; text-decoration: none;
            border-radius: 8px; font-size: 18px;
        }
        .btn:hover { background-color: #555; }
    </style></head><body>
    <h1>Bienvenido al Reporte del Compilador</h1>
    <p>Selecciona una de las opciones para visualizar:</p>
    <div class='btn-container'>
        <a href='tokens.html' class='btn'>📄 Ver Tokens</a>
        <a href='errores.html' class='btn'>🚫 Ver Errores</a>
        <a href='tabla_simbolos.html' class='btn'>📘 Ver Tabla de Simbolos</a>
    </div>
    </body></html>
    """
    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)

def abrir_todos_los_html():
    for archivo in ["index.html", "tokens.html", "errores.html", "tabla_simbolos.html"]:
        abrir_html(archivo)
