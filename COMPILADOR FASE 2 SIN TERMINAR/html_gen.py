import webbrowser
import os

def generar_menu():
    """Genera el menú de navegación común"""
    return """
    <div class='menu'>
        <a href='index.html'>🏠 Inicio</a>
        <a href='tokens.html'>📄 Tokens</a>
        <a href='errores.html'>❌ Errores</a>
        <a href='tabla_simbolos.html'>📘 Tabla de Símbolos</a>
        <a href='codigo_intermedio.txt'>🔧 Código Intermedio</a>
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
    <button class='scroll-top' onclick='window.scrollTo({top: 0, behavior: "smooth"})'>⬆</button>
    """

def generar_pagina_inicio():
    """Genera la página de inicio con navegación mejorada"""
    html_content = """
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
    <h1>🚀 Compilador - Reportes Completos</h1>
    <p>Selecciona una de las opciones para visualizar los resultados del análisis:</p>
    <div class='btn-container'>
        <a href='tokens.html' class='btn'>📄 Ver Tokens</a>
        <a href='errores.html' class='btn'>🚫 Ver Errores</a>
        <a href='tabla_simbolos.html' class='btn'>📘 Ver Tabla de Símbolos</a>
        <a href='codigo_intermedio.txt' class='btn'>🔧 Ver Código Intermedio</a>
    </div>
    </body></html>
    """
    with open("index.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)

def generar_html_tokens(tokens):
    """Genera el archivo HTML con la tabla de tokens"""
    html_content = """
    <html><head><title>Bitácora de Tokens</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #00c853, #43cea2); color: white; }
        h2 { color: white; text-align: center; animation: fadeIn 1s ease-in; }
        table { width: 90%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }
        th, td { border: 1px solid #2e7d32; padding: 12px; text-align: center; }
        th { background-color: #2e7d32; color: white; }
        tr:nth-child(even) { background-color: #f0f0f0; }
        tr:hover { background-color: #dcedc8; }
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
    </style></head><body>
    """ + generar_menu() + """
    <h2>Bitácora de Tokens</h2>
    <table>
        <tr><th>Token</th><th>Valor</th><th>Línea</th><th>Columna</th></tr>
    """

    for token in tokens:
        linea = getattr(token, 'linea', getattr(token, 'lineno', '-'))
        columna = getattr(token, 'columna', getattr(token, 'column', '-'))
        html_content += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{linea}</td><td>{columna}</td></tr>"

    html_content += "</table></body></html>"

    with open("tokens.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)


def generar_html_errores(errores):
    """Genera el archivo HTML con la tabla de errores"""
    html_content = """
    <html><head><title>Bitácora de Errores</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #ff416c, #ff4b2b); color: white; }
        h2 { color: white; text-align: center; animation: fadeIn 1s ease-in; }
        table { width: 95%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }
        th, td { border: 1px solid #b71c1c; padding: 12px; text-align: center; }
        th { background-color: #b71c1c; color: white; }

        .error-lexico { background-color: #ffebee; color: #c62828; font-weight: bold; }
        .error-sintactico { background-color: #fff3e0; color: #ef6c00; font-weight: bold; }
        .error-semantico { background-color: #f3e5f5; color: #7b1fa2; font-weight: bold; }
        .advertencia { background-color: #fff9c4; color: #f57f17; font-weight: bold; }

        tr:hover { background-color: #ffcdd2; }
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }

        .stats {
            background: rgba(255,255,255,0.2);
            padding: 20px;
            margin: 20px auto;
            width: 90%;
            border-radius: 15px;
            text-align: center;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .stats h3 { margin-bottom: 10px; }
        .stats p { font-weight: bold; }
        .stats .count {
            background: rgba(255,255,255,0.2);
            padding: 5px 10px;
            border-radius: 8px;
            margin: 0 5px;
        }
    </style></head><body>
    """ + generar_menu() + """
    <h2>📋 Bitácora de Errores</h2>
    """

    lexicos = sum(1 for e in errores if "Léxico" in e[0])
    sintacticos = sum(1 for e in errores if "sintáctico" in e[0] and "Semántico" not in e[0])
    semanticos = sum(1 for e in errores if "Semántico" in e[0])
    advertencias = sum(1 for e in errores if "Advertencia" in e[0])

    html_content += f"""
    <div class='stats'>
        <h3>📊 Resumen</h3>
        <p>
            <span class='count'>Total: {len(errores)}</span> |
            <span class='count'>Léxicos: {lexicos}</span> |
            <span class='count'>Sintácticos: {sintacticos}</span> |
            <span class='count'>Semánticos: {semanticos}</span> |
            <span class='count'>Advertencias: {advertencias}</span>
        </p>
    </div>
    """

    html_content += "<table><tr><th>Tipo</th><th>Mensaje</th><th>Línea</th><th>Columna</th></tr>"

    for mensaje, linea, columna in errores:
        if "Léxico" in mensaje:
            clase = "error-lexico"; tipo = "Léxico"
        elif "sintáctico" in mensaje and "Semántico" not in mensaje:
            clase = "error-sintactico"; tipo = "Sintáctico"
        elif "Semántico" in mensaje:
            clase = "error-semantico"; tipo = "Semántico"
        elif "Advertencia" in mensaje:
            clase = "advertencia"; tipo = "Advertencia"
        else:
            clase = "error-sintactico"; tipo = "Sintáctico"

        html_content += f"<tr class='{clase}'><td>{tipo}</td><td>{mensaje}</td><td>{linea}</td><td>{columna}</td></tr>"

    html_content += "</table></body></html>"

    with open("errores.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)

def generar_html_tabla_simbolos(tabla_simbolos):
    """Genera el archivo HTML con la tabla de símbolos, estilo conservado"""
    html_content = """
    <html><head><title>Tabla de Símbolos</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(to right, #6a11cb, #2575fc); color: white; }
        h2 { color: white; text-align: center; animation: fadeIn 1s ease-in; }
        table { width: 95%; margin: 30px auto; border-collapse: collapse; background: white; color: black; }
        th, td { border: 1px solid #1565c0; padding: 10px; text-align: center; font-size: 14px; }
        th { background-color: #1565c0; color: white; font-weight: bold; }
        tr:nth-child(even) { background-color: #e3f2fd; }
        tr:nth-child(odd) { background-color: #f8f9fa; }
        tr:hover { background-color: #bbdefb; }
        .usado-si { color: #1565c0; font-weight: bold; }
        .usado-no { color: #757575; font-weight: bold; }
        .funcion { background-color: #e1f5fe; }
        .variable { background-color: #f3e5f5; }
        @keyframes fadeIn { from { opacity: 0 } to { opacity: 1 } }
        .stats { 
            background: rgba(255,255,255,0.2); 
            padding: 15px; 
            margin: 20px auto; 
            width: 90%; 
            border-radius: 10px; 
            text-align: center;
            border: 2px solid rgba(255,255,255,0.3);
        }
        .stats h3, .stats p { color: white; }
    </style></head><body>
    """ + generar_menu() + """
    <h2>📘 Tabla de Símbolos</h2>
    """

    simbolos = tabla_simbolos.mostrar_tabla() if hasattr(tabla_simbolos, 'mostrar_tabla') else []

    # Eliminar la función "inicio" de la vista si existe
    simbolos = [s for s in simbolos if not (s['tipo'] == 'funcion' and s['nombre'] == 'inicio')]

    # Estadísticas
    total_vars = sum(1 for s in simbolos if s['tipo'] != 'funcion')
    total_funcs = sum(1 for s in simbolos if s['tipo'] == 'funcion')
    vars_usadas = sum(1 for s in simbolos if s['tipo'] != 'funcion' and s['usado'])

    html_content += f"""
    <div class='stats'>
        <h3>📈 Estadísticas de Símbolos</h3>
        <p>Variables: {total_vars} | Funciones: {total_funcs} | Variables Usadas: {vars_usadas}/{total_vars}</p>
    </div>
    """

    html_content += """
    <table>
        <tr>
            <th>Nombre</th>
            <th>Tipo</th>
            <th>Ámbito</th>
            <th>Valor</th>
            <th>Usado</th>
            <th>Modificable</th>
            <th>Línea</th>
            <th>Columna</th>
            <th>Detalles</th>
        </tr>
    """

    for simbolo in simbolos:
        clase_fila = "funcion" if simbolo['tipo'] == 'funcion' else "variable"
        usado_texto = "✅ Sí" if simbolo.get('usado') else "❌ No"
        usado_clase = "usado-si" if simbolo.get('usado') else "usado-no"
        modificable_texto = "✅ Sí" if simbolo.get('modificable', True) else "❌ No"
        detalles = ""

        if simbolo['tipo'] == 'funcion' and simbolo.get('parametros'):
            params = simbolo['parametros']
            if params:
                param_str = ", ".join([f"{p[1]} {p[0]}" for p in params])
                detalles = f"Parámetros: {param_str}"
            else:
                detalles = "Sin parámetros"
        else:
            detalles = f"Tipo: {simbolo['tipo']}"

        html_content += f"""
        <tr class='{clase_fila}'>
            <td><strong>{simbolo['nombre']}</strong></td>
            <td>{simbolo['tipo']}</td>
            <td>{simbolo['ambito']}</td>
            <td>{simbolo.get('valor', 'N/A')}</td>
            <td class='{usado_clase}'>{usado_texto}</td>
            <td>{modificable_texto}</td>
            <td>{simbolo.get('linea', '-')}</td>
            <td>{simbolo.get('columna', '-')}</td>
            <td><small>{detalles}</small></td>
        </tr>
        """

    html_content += "</table></body></html>"

    with open("tabla_simbolos.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)

def abrir_html(archivo):
    """Abre el archivo HTML en el navegador"""
    ruta_completa = os.path.abspath(archivo)
    webbrowser.open(f"file://{ruta_completa}")
    print(f"✅ Abriendo {archivo} en el navegador...")