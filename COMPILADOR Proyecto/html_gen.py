# html_gen.py

def generar_html(tokens):
    html_content = "<html><head><title>Tokens Analizados</title></head><body>"
    html_content += "<h1>Lista de Tokens</h1><table border='1'><tr><th>Token</th><th>Valor</th><th>Linea</th></tr>"

    for token in tokens:
        html_content += f"<tr><td>{token.type}</td><td>{token.value}</td><td>{token.lineno}</td></tr>"

    html_content += "</table></body></html>"

    with open("tokens.html", "w", encoding="utf-8") as archivo:
        archivo.write(html_content)

    print("Archivo HTML generado exitosamente: tokens.html")