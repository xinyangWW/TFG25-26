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


def normalizar_respuesta(respuesta: str) -> str:
    """
    Normaliza la respuesta del modelo a una cadena canónica:
      - "R"           → todos los reales
      - "NO_SOLUTION" → sin solución
      - "ERROR"       → error técnico del modelo
      - "1,2,3"       → lista de números ordenada y deduplicada
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

    # ── 3. Extraer números ───────────────────────────────────────────────────
    numeros = re.findall(r"-?\d+(?:\.\d+)?", r)
    if numeros:
        nums = sorted(set(float(n) for n in numeros))
        nums = [int(n) if n.is_integer() else n for n in nums]
        return ",".join(str(n) for n in nums)

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
