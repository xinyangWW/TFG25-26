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


def caso_7_diferencia_cuadrados_no_nula():
    """
    MR: Reescribir una diferencia de cuadrados en forma expandida
    no cambia las soluciones de la ecuación.
    (x - 5)(x + 5) = 24 → x^2 - 25 = 24.
    Resultado esperado: x = 7 y x = -7.
    """
    prompt_base = (
        "Resuelve la ecuación: (x - 5)(x + 5) = 24. "
        "Responde solo con las soluciones, en español."
    )

    prompt_transformado = (
        "Resuelve la ecuación: x^2 - 25 = 24. "
        "Responde solo con las soluciones, en español."
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
        caso="Caso 7: Diferencia de cuadrados no nula",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 7: Diferencia de cuadrados no nula",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_7_diferencia_cuadrados_no_nula()