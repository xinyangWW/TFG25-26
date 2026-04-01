import re

# Función para normalizar la salida
def normalizar_respuesta(respuesta: str) -> str:
    if not respuesta:
        return ""

    r = respuesta.strip().lower()
    
    # eliminar etiquetas tipo </think>
    r = re.sub(r"</?think>", "", r)

    # eliminar símbolos latex
    r = r.replace("\\(", "").replace("\\)", "")

    # detectar reales
    if re.search(r"(x\s*[∈e]\s*[rℝ])|(todos los reales)|(números reales)|(numeros reales)", r):
        return "R"

    if any(x in r for x in [
        "sin solución",
        "sin solucion",
        "no tiene solución",
        "no tiene solucion",
        "no hay solución",
        "no hay solucion",
        "conjunto vacío",
        "conjunto vacio",
        "∅"
    ]):
        return "NO_SOLUTION"

    numeros = re.findall(r"-?\d+(?:\.\d+)?", r)
    if numeros:
        # Tomar solo el ÚLTIMO número (el resultado final)
        ultimo_numero = float(numeros[-1])
        if ultimo_numero.is_integer():
            return str(int(ultimo_numero))
        else:
            return str(ultimo_numero)

    return r

# Función principal para evaluar si se cumple la relación metamorfica
def evaluar_cumplimiento_mr(respuesta_base: str, respuesta_transformada: str):
    """
    Devuelve:
    - cumple_mr
    - error_tecnico
    """

    base_norm = normalizar_respuesta(respuesta_base)
    transf_norm = normalizar_respuesta(respuesta_transformada)

    error_tecnico = (
        base_norm == ""
        or transf_norm == ""
    )

    cumple_mr = (
        not error_tecnico
        and base_norm == transf_norm
    )

    return cumple_mr, error_tecnico