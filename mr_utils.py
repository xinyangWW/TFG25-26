import re
from sympy import sympify, integrate, symbols, Symbol, diff, solveset, S, simplify

# ── Patrones de "sin solución" (solo español) ────────────────────────────────
_NO_SOLUTION_PATTERNS = [
    "sin solución", "sin solucion",
    "no tiene solución", "no tiene solucion",
    "no hay solución", "no hay solucion",
    "no existe solución", "no existe solucion",
    "conjunto vacío", "conjunto vacio",
    "∅",
]

# ── Patrones de "todos los reales" (solo español) ────────────────────────────
_REAL_PATTERN = re.compile(
    r"(x\s*[∈e]\s*[rℝ])"
    r"|(todos los reales)"
    r"|(números reales|numeros reales)"
)

# ── Fracciones escritas en español ───────────────────────────────────────────
# Mapea expresiones textuales a su valor decimal
_FRACCIONES_TEXTO = {
    # mitades
    "un medio": 0.5, "una mitad": 0.5,
    # tercios
    "un tercio": round(1/3, 10), "dos tercios": round(2/3, 10),
    # cuartos
    "un cuarto": 0.25, "tres cuartos": 0.75,
    # quintos
    "un quinto": 0.2, "dos quintos": 0.4,
    "tres quintos": 0.6, "cuatro quintos": 0.8,
    # sextos
    "un sexto": round(1/6, 10), "cinco sextos": round(5/6, 10),
    # séptimos
    "un séptimo": round(1/7, 10), "un septimo": round(1/7, 10),
    # octavos
    "un octavo": 0.125, "tres octavos": 0.375,
    "cinco octavos": 0.625, "siete octavos": 0.875,
    # novenos
    "un noveno": round(1/9, 10),
    # décimos
    "un décimo": 0.1, "un decimo": 0.1,
    "tres décimos": 0.3, "tres decimos": 0.3,
    "siete décimos": 0.7, "siete decimos": 0.7,
    "nueve décimos": 0.9, "nueve decimos": 0.9,
}


def _fraccion_a_decimal(texto: str) -> float | None:
    """
    Intenta convertir una fracción en formato 'a/b' a decimal.
    Devuelve None si no encuentra ninguna fracción.
    Busca la ÚLTIMA fracción válida en el texto (el resultado final).
    """
    # Busca patrones del tipo número/número, evitando falsos positivos como fechas
    matches = re.findall(r"(-?\d+)\s*/\s*(\d+)", texto)
    if matches:
        num, den = matches[-1]  # última fracción encontrada
        den = int(den)
        if den != 0:
            return int(num) / den
    return None


def normalizar_respuesta(respuesta: str) -> str:
    """
    Normaliza la respuesta del modelo a una cadena canónica:
      - "R"           → todos los reales
      - "NO_SOLUTION" → sin solución
      - "ERROR"       → error técnico del modelo
      - número        → último número encontrado (entero o decimal)
      - fracción a/b  → convertida a decimal
      - texto fracción → "cuatro quintos" → 0.8
      - texto limpio  → cualquier otro caso
    """
    if not respuesta:
        return ""

    # Detectar errores técnicos devueltos por query_model
    if respuesta.startswith("[ERROR"):
        return "ERROR"

    r = respuesta.strip().lower()

    # Eliminar etiquetas tipo <think> / </think>
    r = re.sub(r"</?think>", "", r)

    # Eliminar símbolos LaTeX inline
    r = r.replace("\\(", "").replace("\\)", "")
    r = re.sub(r"\$+", "", r)
    r = re.sub(r"\s+", " ", r).strip()

    # ── 1. Sin solución ──────────────────────────────────────────────────────
    if any(p in r for p in _NO_SOLUTION_PATTERNS):
        return "NO_SOLUTION"

    # ── 2. Todos los reales ──────────────────────────────────────────────────
    if _REAL_PATTERN.search(r):
        return "R"

    # ── 3. Fracciones escritas en español ────────────────────────────────────
    for expresion, valor in _FRACCIONES_TEXTO.items():
        if expresion in r:
            return str(int(valor)) if float(valor).is_integer() else str(valor)

    # ── 4. Fracciones en formato a/b ─────────────────────────────────────────
    valor_fraccion = _fraccion_a_decimal(r)
    if valor_fraccion is not None:
        return str(int(valor_fraccion)) if float(valor_fraccion).is_integer() else str(round(valor_fraccion, 10))

    # ── 5. Extraer números SIEMPRE que existan ─────────────────────────────
    numeros = re.findall(r"-?\d+(?:\.\d+)?", r)

    if numeros:
        valores = sorted(float(n) for n in numeros)
        valores_str = [
            str(int(v)) if v.is_integer() else str(v)
            for v in valores
        ]
        return ",".join(valores_str)

    # ── 6. Fallback: texto limpio ─────────────────────────────────────────
    r = r.replace(" ", "")
    r = r.replace("*", "")
    return r


def evaluar_cumplimiento_mr(respuesta_base: str, respuesta_transformada: str):
    """
    Compara dos respuestas normalizadas y devuelve:
      - cumple_mr     (bool): True si ambas normalizaciones coinciden
      - error_tecnico (bool): True si alguna respuesta está vacía o es ERROR
    """
    base_norm   = normalizar_respuesta(respuesta_base)
    transf_norm = normalizar_respuesta(respuesta_transformada)

    error_tecnico = (
        base_norm in ("", "ERROR")
        or transf_norm in ("", "ERROR")
    )

    if error_tecnico:
        return False, True

    # trata de comparar como números y compara con cierta tolerancia
    try:
        base_val = float(base_norm)
        transf_val = float(transf_norm)
        epsilon = 1e-4
        cumple_mr = abs(base_val - transf_val) < epsilon
    # si no son números, compara como texto
    except ValueError:
        cumple_mr = base_norm == transf_norm

    return cumple_mr, False

# extrae números positivos o negativos, enteros o decimales, de un string
def extraer_valores(respuesta: str):
    numeros = re.findall(r"-?\d+(?:\.\d+)?", respuesta)
    return [float(n) for n in numeros]


# formatea una lista de valores con sus variables correspondientes
def formatear_lista_valores(valores, variable):
    if not valores:
        return "valores inválidos"

    return ", ".join(f"{variable} = {int(v) if v.is_integer() else v}" for v in valores)

# evalúa una ecuación igualando a 0
def evaluar_ecuacion(expr: str, valores: dict):
    try:
        if "=" in expr:
            izq, der = expr.split("=")
            expr = f"({izq}) - ({der})"

        ecuacion = sympify(expr)
        return float(ecuacion.subs(valores))
    except:
        return None

def extraer_soluciones(respuesta: str, variables):
    if not respuesta:
        return None

    # extraer números, también fracciones
    matches = re.findall(r"-?\d+/\d+|-?\d+(?:\.\d+)?", respuesta)

    if not matches:
        return None

    valores = []
    for val in matches:
        if "/" in val:
            num, den = val.split("/")
            valores.append(float(num) / float(den))
        else:
            valores.append(float(val))

    # agrupar en bloques del tamaño de variables
    n = len(variables)

    if len(valores) % n != 0:
        return None 

    soluciones = []
    for i in range(0, len(valores), n):
        bloque = valores[i:i+n]
        soluciones.append(dict(zip(variables, bloque)))

    return soluciones

# para el prompt transformado
def formatear_soluciones(soluciones):
    if not soluciones:
        return "valores inválidos"

    partes = []
    for sol in soluciones:
        parte = ", ".join(f"{k} = {int(v) if v.is_integer() else v}" for k, v in sol.items())
        partes.append(f"({parte})")

    return " ; ".join(partes)

# evalúa una ecuación o sistema de ecuaciones dado una serie de valores para las variables
def evaluar_solucion_general(respuesta_modelo: str, ecuaciones, variables=('x',), epsilon=1e-6):
    if not respuesta_modelo or respuesta_modelo.startswith("[ERROR"):
        return False, True

    soluciones = extraer_soluciones(respuesta_modelo, variables)

    if not soluciones:
        return False, True

    for valores in soluciones:
        for eq in ecuaciones:
            resultado = evaluar_ecuacion(eq, valores)

            if resultado is None or abs(resultado) > epsilon:
                return False, False

    return True, False

# funcion que evalúa una integral definida
def evaluar_integral_definida(expr: str, variable: str, a: float, b: float, valor_modelo: float, epsilon=1e-5):
    try:
        var = symbols(variable)

        # parsear expresión
        funcion = sympify(expr)

        # calcular integral exacta
        resultado_real = float(integrate(funcion, (var, a, b)))

        return abs(resultado_real - valor_modelo) < epsilon

    except:
        return None
    
# función que evalúa la respuesta del modelo para una integral definida
def evaluar_integral_respuesta(respuesta_modelo: str, expr: str, variable: str, a: float, b: float, epsilon=1e-6):
    if not respuesta_modelo or respuesta_modelo.startswith("[ERROR"):
        return False, True

    valores = re.findall(r"-?\d+/\d+|-?\d+(?:\.\d+)?", respuesta_modelo)

    if not valores:
        return False, True

    val = valores[-1]

    if "/" in val:
        num, den = val.split("/")
        val = float(num) / float(den)
    else:
        val = float(val)

    correcto = evaluar_integral_definida(expr, variable, a, b, val, epsilon)

    if correcto is None:
        return False, True

    return correcto, False

# función que extrae una matriz en formato cadena entre corchetes y la convierte de una lista de listas de float
def extraer_matriz(respuesta: str):
    filas = re.findall(r"\[([^\[\]]+)\]", respuesta)

    matriz = []
    for fila in filas:
        nums = re.findall(r"-?\d+(?:\.\d+)?", fila)
        if nums:
            matriz.append([float(n) for n in nums])

    return matriz if matriz else None

# función para multiplicar dos matrices
def multiplicar_matrices(A, B):
    resultado = []

    for i in range(len(A)):
        fila = []
        for j in range(len(B[0])):
            val = sum(A[i][k] * B[k][j] for k in range(len(B)))
            fila.append(val)
        resultado.append(fila)

    return resultado

# función para comprobar si una matriz es la identidad
def es_matriz_identidad(M):
    n = len(M)

    for i in range(n):
        for j in range(n):
            if i == j:
                if M[i][j] != 1:
                    return False
            else:
                if M[i][j] != 0:
                    return False

    return True

# función para comparar dos matrices
def matrices_iguales(A, B, epsilon=1e-6):
    if not A or not B:
        return False

    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            if abs(A[i][j] - B[i][j]) > epsilon:
                return False

    return True

# función para evalúar el valor de una función en un punto y comprobar si es un extremo absoluto
def evaluar_extremo_global(respuesta_modelo: str, funcion: str, tipo="max", epsilon=1e-6):

    x = Symbol('x')

    puntos = extraer_valores(respuesta_modelo)
    if not puntos:
        return False, True

    x0 = float(puntos[-1])

    try:
        f = sympify(funcion)
        f1 = diff(f, x)

        # puntos críticos
        criticos = solveset(f1, x, domain=S.Reals)

        if not criticos:
            return False, False

        f_x0 = float(f.subs(x, x0))

        # evaluar SOLO en críticos
        valores = [
            float(f.subs(x, c))
            for c in criticos
            if c.is_real
        ]

        if tipo == "max":
            return all(f_x0 >= v - epsilon for v in valores), False

        elif tipo == "min":
            return all(f_x0 <= v + epsilon for v in valores), False

        else:
            return False, True

    except:
        return False, True

# funcion para comprobar que dos expresiones simbólicas son iguales
def equivalentes(expr1, expr2):
    try:
        return simplify(sympify(expr1) - sympify(expr2)) == 0
    except Exception as e:
        return False
    
# funcion para evaluar el cumplimiento de mr, cuando queremos comparar expresiones
def evaluar_cumplimiento_expresiones(base, transf):
    try:
        return equivalentes(base, transf), False
    except:
        return False, True
    
