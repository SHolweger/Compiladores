class SymbolTable:
    def __init__(self):
        self.tabla_simbolos = {}   # (nombre, ambito) -> metadata
        self.errors = []
        self.scopes = ['global']
        self._local_counter = 0
        self._function_scope = None

    def entrar_ambito(self, tipo="bloque"):
        self._local_counter += 1
        if tipo == "funcion":
            amb = f"funcion#{self._local_counter}"
            self._function_scope = amb
        elif tipo == "parametros":
            amb = self._function_scope or f"funcion#{self._local_counter}"
        else:
            amb = f"bloque#{self._local_counter}"
        self.scopes.append(amb)
        return amb

    def salir_ambito(self):
        if len(self.scopes) > 1:
            out = self.scopes.pop()
            if out.startswith("funcion#"):
                self._function_scope = None

    def obtener_ambito(self):
        return self.scopes[-1]

    def agregar_simbolo(self, nombre, tipo, valor_original, linea, columna,
                       modificable=True, parametros=None, retorno=None):
        amb = self.obtener_ambito()
        key = (nombre, amb)
        if key in self.tabla_simbolos:
            self.errors.append((f"Error Semántico: '{nombre}' ya declarado en {amb}.", linea, columna))
            return False
        # Guardamos el nodo AST en valor_original, no lo evaluamos aquí
        self.tabla_simbolos[key] = {
            'tipo': tipo,
            'valor_original': valor_original,
            'valor': None,  # se llenará tras interpretación
            'linea': linea,
            'columna': columna,
            'ambito': amb,
            'modificable': modificable,
            'usado': False,
            'parametros': parametros or [],
            'retorno': retorno
        }
        return True

    def buscar_simbolo(self, nombre, linea, columna):
        for amb in reversed(self.scopes):
            key = (nombre, amb)
            if key in self.tabla_simbolos:
                self.tabla_simbolos[key]['usado'] = True
                return self.tabla_simbolos[key]
        self.errors.append((f"Error Semántico: Variable '{nombre}' no declarada.", linea, columna))
        return None

    def actualizar_simbolo(self, nombre, valor, linea, columna):
        for amb in reversed(self.scopes):
            key = (nombre, amb)
            if key in self.tabla_simbolos:
                if not self.tabla_simbolos[key]['modificable']:
                    self.errors.append((f"Error Semántico: '{nombre}' no modificable.", linea, columna))
                    return False
                # tras interpretar, guardamos el valor real
                self.tabla_simbolos[key]['valor'] = valor
                self.tabla_simbolos[key]['usado'] = True
                return True
        self.errors.append((f"Error Semántico: Variable '{nombre}' no declarada.", linea, columna))
        return False

    def mostrar_tabla(self):
        rows = []
        for (nombre, amb), m in self.tabla_simbolos.items():
            rows.append({
                'nombre': nombre,
                'tipo': m['tipo'],
                'ambito': amb,
                'valor': m['valor'] if m['valor'] is not None else "Sin inicializar",
                'linea': m['linea'],
                'columna': m['columna'],
                'usado': m['usado']
            })
        return rows
