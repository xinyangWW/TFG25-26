import sys
import os

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)
import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"
TIPO = "Algebraica"


def caso_30_sustitucion_variable(offset: int):
    """
    MR: Renombrar la variable en una ecuación no cambia la solución numérica.
    x^2 - offset^2 = 0  con variable x  →  misma ecuación con variable t.
    Solución positiva esperada: offset.
    """
    prompt_base = (
        f"Resuelve la ecuación: x^2 - {offset**2} = 0. "
        "Indica solo la solución positiva. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación: t^2 - {offset**2} = 0. "
        "Indica solo la solución positiva. "
        "Responde solo con la respuesta, en español."
    )

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 30: Sustitución de variable — x^2={offset**2} vs t^2={offset**2}, solución positiva",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 30: Sustitución de variable — x^2={offset**2} vs t^2={offset**2}, solución positiva",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_30_sustitucion_variable(5)    # x^2 = 25 → x = 5
    caso_30_sustitucion_variable(8)    # x^2 = 64 → x = 8
    caso_30_sustitucion_variable(11)   # x^2 = 121 → x = 11
