# 🚀 Compilador de Lenguaje Español

Un compilador completo desarrollado en Python que procesa un lenguaje de programación con sintaxis en español. Implementa todas las fases de compilación: análisis léxico, sintáctico, semántico y generación de código intermedio.

## ��� Características

### ✅ Análisis Léxico
- Reconocimiento de tokens en español
- Detección de errores léxicos
- Generación de bitácora de tokens con posiciones

### ✅ Análisis Sintáctico  
- Parser LR(1) usando PLY (Python Lex-Yacc)
- Construcción de AST (Árbol de Sintaxis Abstracta)
- Manejo de errores sintácticos con recuperación

### ✅ Análisis Semántico
- Tabla de símbolos con manejo de ámbitos
- Verificación de tipos
- Detección de variables no declaradas/no usadas
- Validación de llamadas a funciones

### ✅ Generación de Código
- Código intermedio de tres direcciones
- Optimización básica de expresiones
- Manejo de estructuras de control

### ✅ Reportes y Visualización
- Reportes HTML interactivos
- Menú interactivo en consola
- Simulador básico de ejecución

## 🛠️ Dependencias

\`\`\`bash
pip install ply
\`\`\`

## 📁 Estructura del Proyecto

\`\`\`
Compilador - Fase 1 2 3/
├── main_interactive.py      # Punto de entrada principal
├── interactive_menu.py      # Menú interactivo
├── lexer_module.py         # Analizador léxico
├── parser_module.py        # Analizador sintáctico
├── semantic_module.py      # Analizador semántico
├── code_generator.py       # Generador de código intermedio
├── ast_nodes.py           # Definición de nodos AST
├── tabla_simbolos.py      # Tabla de símbolos
├── html_gen.py           # Generador de reportes HTML
├── main.py               # Versión simple (solo análisis)
└── codigo_fuente.txt     # Archivo de ejemplo
\`\`\`

## 🚀 Uso

### Menú Interactivo (Recomendado)
\`\`\`bash
python main_interactive.py
\`\`\`

### Análisis Directo
\`\`\`bash
python main.py
\`\`\`

## 📝 Sintaxis del Lenguaje

### Variables
\`\`\`javascript
numero x = 5;
decimal pi = 3.14159;
cadena nombre = "Juan";
booleano activo = verdadero;
\`\`\`

### Funciones
\`\`\`javascript
funcion calcular(numero a, numero b) {
    numero resultado = a + b;
    regresa resultado;
}

inicio() {
    numero x = 10;
    numero y = 20;
    numero suma = calcular(x, y);
    mostrar(suma);
}
\`\`\`

### Estructuras de Control
\`\`\`javascript
// Condicionales
si (x > 0) {
    mostrar("Positivo");
} sino {
    mostrar("No positivo");
}

// Bucles
mientras (i < 10) {
    mostrar(i);
    i = i + 1;
}

// For
para (numero i = 0; i < 10; i = i + 1) {
    mostrar(i);
}

// Do-While
repetir {
    mostrar("Hola");
    i = i + 1;
} hasta (i >= 5);
\`\`\`

### Switch
\`\`\`javascript
cambiar (opcion) {
    caso 1: mostrar("Uno"); break;
    caso 2: mostrar("Dos"); break;
    predeterminado: mostrar("Otro");
}
\`\`\`

## 🎯 Funcionalidades del Menú

1. **📁 Seleccionar archivo fuente** - Carga un archivo de código
2. **🔍 Analizar código completo** - Ejecuta todas las fases de análisis
3. **📄 Ver tokens** - Muestra la lista de tokens encontrados
4. **❌ Ver errores** - Muestra errores y advertencias
5. **📘 Ver tabla de símbolos** - Muestra variables y funciones declaradas
6. **⚙️ Ver código intermedio** - Muestra código de 3 direcciones generado
7. **🌐 Generar reportes HTML** - Crea reportes visuales en HTML
8. **🔄 Ejecutar simulación** - Simula la ejecución del código
9. **📖 Ayuda** - Muestra información de ayuda

## 📊 Reportes HTML

El compilador genera reportes HTML interactivos:

- **index.html** - Página principal con navegación
- **tokens.html** - Bitácora detallada de tokens
- **errores.html** - Lista de errores y advertencias
- **tabla_simbolos.html** - Tabla de símbolos completa
- **codigo_intermedio.html** - Código de tres direcciones

## 🔧 Código Intermedio

El generador produce código de tres direcciones optimizado:

\`\`\`
1: function inicio:
2: declare numero x
3: x = 5
4: declare numero y  
5: y = 10
6: t1 = x + y
7: print t1
8: end function inicio
\`\`\`

## 🧪 Ejemplo de Uso

1. Ejecutar `python main_interactive.py`
2. Seleccionar opción 1 para cargar archivo
3. Seleccionar opción 2 para analizar
4. Usar opciones 3-8 para ver resultados
5. Opción 7 para generar reportes HTML

## 🐛 Manejo de Errores

El compilador detecta y reporta:

- **Errores léxicos**: Caracteres no reconocidos
- **Errores sintácticos**: Estructura incorrecta
- **Errores semánticos**: Tipos incompatibles, variables no declaradas
- **Advertencias**: Variables declaradas pero no usadas

## 🎓 Basado en

- **Libro**: "Compiladores: Principios, Técnicas y Herramientas" (Libro del Dragón)
- **Autores**: Alfred V. Aho, Monica S. Lam, Ravi Sethi, Jeffrey D. Ullman
- **Herramientas**: PLY (Python Lex-Yacc)

## 👨‍💻 Desarrollo

Este compilador fue desarrollado como proyecto académico, implementando:

- Análisis léxico con expresiones regulares
- Parser LR(1) con manejo de precedencia
- Análisis semántico con tabla de símbolos jerárquica
- Generación de código intermedio optimizado
- Interfaz de usuario interactiva

## 📈 Características Avanzadas

- **Manejo de ámbitos**: Variables locales y globales
- **Verificación de tipos**: Compatibilidad en operaciones
- **Optimización**: Eliminación de código muerto
- **Recuperación de errores**: Continúa análisis tras errores
- **Reportes visuales**: HTML con CSS y animaciones

## 🔮 Extensiones Futuras

- Generación de código objeto
- Optimizaciones avanzadas
- Soporte para arrays y estructuras
- Depurador integrado
- IDE con resaltado de sintaxis

---

**Desarrollado con ❤️ para el aprendizaje de compiladores**
