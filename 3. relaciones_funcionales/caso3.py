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
TIPO = "Relaciones funcionales"


def caso_3_reescritura_algebraica():
    """
    MR: Reescribir la fórmula de forma algebraicamente equivalente no cambia el resultado.
    f(x) = x^2 - 9  →  f(x) = (x-3)(x+3).
    Evaluamos f(5). Resultado esperado: 16.
    """
    prompt_base = (
        "Sea f(x) = x^2 - 9. Calcula f(5). "
        "Responde solo con el número, en español."
    )
    prompt_transformado = (
        "Sea f(x) = (x - 3)(x + 3). Calcula f(5). "
        "Responde solo con el número, en español."
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
        caso="Caso 3 Funcional: Reescritura algebraica — f(5) con x^2-9 vs (x-3)(x+3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 3 Funcional: Reescritura algebraica — f(5) con x^2-9 vs (x-3)(x+3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_3_reescritura_algebraica()
