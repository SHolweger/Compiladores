class SymbolTable:
    def __init__(self):
        self.tabla_simbolos = {}     # clave: (nombre, ambito) -> metadata
        self.errors = []
        self.scopes = ['global']
        self._local_counter = 0      # contador de bloques “local”

    # --- Manejo de ámbitos ---
    def entrar_ambito(self):
        """Crea un nuevo ámbito local único y lo pone en la pila."""
        self._local_counter += 1
        ambito = f"local#{self._local_counter}"
        self.scopes.append(ambito)
        
        return ambito

    def salir_ambito(self):
        print("Saliendo de ambito:", self.scopes[-1])
        """Sale del ámbito actual (si no es el global)."""
        if len(self.scopes) > 1:
            self.scopes.pop()
            

    def obtener_ambito_interno(self):
        """Devuelve el nombre interno del ámbito en la cima de la pila."""
        interno = self.scopes[-1]
        print("Obteniendo ambito interno:", interno)
        return interno

    def obtener_ambito_para_mostrar(self):
        """Mapa el nombre interno a la etiqueta "local" o mantiene global."""
        interno = self.scopes[-1]
        print("Obteniendo ambito para mostrar:", interno)
        return 'local' if interno.startswith('local#') else interno

    # --- Declarar símbolo ---
    def agregar_simbolo(self, nombre, tipo, valor, linea, columna, modificable=True, parametros=None, retorno=None):
        interno = self.obtener_ambito_interno()
        key = (nombre, interno)
        if key in self.tabla_simbolos:
            self.errors.append((
                f"Error: La variable '{nombre}' ya ha sido declarada en el ámbito '{self.obtener_ambito_para_mostrar()}'.",
                linea, columna
            ))
        else:
            self.tabla_simbolos[key] = {
                'tipo': tipo,
                'valor': valor,
                'linea': linea,
                'columna': columna,
                'ambito': interno,
                'referencia': self.obtener_ambito_para_mostrar(),
                'modificable': modificable,
                'usado': False,
                'parametros': parametros,
                'retorno': retorno
            }

    # --- Buscar y marcar uso ---
    def buscar_simbolo(self, nombre, linea, columna):
        for scope in reversed(self.scopes):
            key = (nombre, scope)
            if key in self.tabla_simbolos:
                self.tabla_simbolos[key]['usado'] = True
                return self.tabla_simbolos[key]
        self.errors.append((f"Variable '{nombre}' no declarada.", linea, columna))
        return None

    # --- Actualizar valor ---
    def actualizar_simbolo(self, nombre, valor, linea, columna):
        entry = self.buscar_simbolo(nombre, linea, columna)
        if not entry:
            return
        if not entry['modificable']:
            self.errors.append((f"Variable '{nombre}' no modificable.", linea, columna))
            return
        entry['valor'] = valor

    # --- Detectar no usados (advertencias) ---
    def verificar_uso_variables(self):
        for (nombre, _), meta in self.tabla_simbolos.items():
            if not meta['usado']:
                self.errors.append((
                    f"Advertencia: '{nombre}' declarado pero no usado.",
                    meta['linea'], meta['columna']
                ))

    def all_symbols(self):
        return self.tabla_simbolos
