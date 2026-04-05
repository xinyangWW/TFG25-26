import re

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

    # ── 5. Extraer el último número (resultado final) ────────────────────────
    numeros = re.findall(r"-?\d+(?:\.\d+)?", r)
    if numeros:
        ultimo = float(numeros[-1])
        return str(int(ultimo)) if ultimo.is_integer() else str(ultimo)

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
        base_norm  in ("", "ERROR")
        or transf_norm in ("", "ERROR")
    )

    cumple_mr = (
        not error_tecnico
        and base_norm == transf_norm
    )

    return cumple_mr, error_tecnico
