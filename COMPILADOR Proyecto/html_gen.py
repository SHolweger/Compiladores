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
        <a href='tabla_simbolos.html'>📘 Tabla de Símbolos</a>
        <button onclick='window.print()'>🖨️ Exportar PDF</button>
    </div>
    <style>
        .menu {
            text-align: center;
            margin: 20px;
            animation: slide-in 0.8s ease-in-out;
        }
        .menu a, .menu button {
            margin: 0 10px;
            padding: 8px 16px;
            background: #ffffff33;
            color: white;
            border: 1px solid white;
            border-radius: 5px;
            text-decoration: none;
            font-weight: bold;
            transition: background 0.3s ease, transform 0.3s ease;
            font-size: 15px;
        }
        .menu a:hover, .menu button:hover {
            background: #ffffff66;
            cursor: pointer;
            transform: scale(1.05) rotate(-1deg);
        }
        @keyframes slide-in {
            from { transform: translateY(-30px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }

        .scroll-top {
            position: fixed;
            bottom: 30px;
            right: 30px;
            padding: 12px 18px;
            background-color: #ffffff44;
            border: 2px solid white;
            border-radius: 50%;
            font-size: 20px;
            color: white;
            cursor: pointer;
            z-index: 1000;
            transition: background 0.3s ease, transform 0.3s ease;
            animation: bounce-in 1s ease forwards;
        }
        .scroll-top:hover {
            background-color: #ffffff88;
            transform: scale(1.2);
        }
        @keyframes bounce-in {
            0%   { transform: translateY(100px); opacity: 0; }
            60%  { transform: translateY(-10px); opacity: 1; }
            80%  { transform: translateY(5px); }
            100% { transform: translateY(0); }
        }
    </style>
    <button class='scroll-top' onclick='window.scrollTo({top: 0, behavior: \"smooth\"})'>⬆</button>
    """

def generar_html_tokens(tokens, nombre_archivo="tokens.html"):
    html = f"""
    <html><head><title>Bitácora de Tokens</title>
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
    <h2>Bitácora de Tokens</h2><table><tr><th>Token</th><th>Valor</th><th>Línea</th><th>Columna</th></tr>
    """
    for token in tokens:
        html += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{token.lineno}</td><td>{token.column}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
 #   abrir_html(nombre_archivo)

def generar_html_errores(errores, nombre_archivo="errores.html"):
    html = f"""
    <html><head><title>Bitácora de Errores</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #ff416c, #ff4b2b); color: white; }}
        h2 {{ color: white; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 90%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }}
        th, td {{ border: 1px solid #b71c1c; padding: 12px; text-align: center; }}
        th {{ background-color: #b71c1c; color: white; }}
        tr:nth-child(even) {{ background-color: #fce4ec; }}
        tr:hover {{ background-color: #ffcdd2; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Bitácora de Errores</h2><table><tr><th>Mensaje</th><th>Línea</th><th>Columna</th></tr>
    """
    for error in errores:
        mensaje = error[0]
        linea = error[1] if len(error) > 1 else -1
        columna = error[2] if len(error) > 2 else -1
        html += f"<tr><td>{mensaje}</td><td>{linea}</td><td>{columna}</td></tr>"
    html += "</table></body></html>"

    with open(nombre_archivo, "w", encoding="utf-8") as file:
        file.write(html)
    abrir_html(nombre_archivo)

def generar_html_tabla_simbolos(tabla_simbolos, nombre_archivo="tabla_simbolos.html"):
    html = f"""
    <html><head><title>Tabla de Símbolos</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #6a11cb, #2575fc); color: white; }}
        h2 {{ color: white; text-align: center; animation: fadeIn 1s ease-in; }}
        table {{ width: 90%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }}
        th, td {{ border: 1px solid #1565c0; padding: 12px; text-align: center; }}
        th {{ background-color: #1565c0; color: white; }}
        tr:nth-child(even) {{ background-color: #e3f2fd; }}
        tr:hover {{ background-color: #bbdefb; }}
        @keyframes fadeIn {{ from {{ opacity: 0 }} to {{ opacity: 1 }} }}
    </style></head><body>
    {generar_menu()}
    <h2>Tabla de Símbolos</h2>
    <table>
        <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Referencia</th>
            <th>Valor</th>
            <th>Línea</th>
            <th>Columna</th>
        </tr>
    """
    for nombre, datos in tabla_simbolos.items():
        html += f"""
        <tr>
            <td>{nombre}</td>
            <td>{datos['tipo']}</td>
            <td>{datos['referencia']}</td>
            <td>{datos['valor']}</td>
            <td>{datos['linea']}</td>
            <td>{datos['columna']}</td>
        </tr>
        """
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
            background-color: #ffffff22; color: white; text-decoration: none;
            border: 1px solid white;
            border-radius: 6px; font-size: 16px;
            transition: background-color 0.3s ease, transform 0.3s ease;
        }
        a.btn:hover { background-color: #ffffff44; transform: scale(1.1); }
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
#    abrir_html(nombre_archivo)

def abrir_todos_los_html():
    generar_pagina_inicio()
    abrir_html("tokens.html")
    abrir_html("errores.html")
    abrir_html("tabla_simbolos.html")
