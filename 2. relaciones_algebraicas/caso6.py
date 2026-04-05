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


def caso_6_cuadrado_binomio():
    """
    MR: Expandir el cuadrado de un binomio no cambia las soluciones de la ecuación.
    (x + 2)^2 = 9 → x^2 + 4x + 4 = 9.
    Resultado esperado: x = 1 y x = -5.
    """
    prompt_base = (
        "Resuelve la ecuación: (x + 2)^2 = 9. "
        "Responde solo con las soluciones, en español."
    )

    prompt_transformado = (
        "Resuelve la ecuación: x^2 + 4x + 4 = 9. "
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
        caso="Caso 6: Cuadrado de binomio",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 6: Cuadrado de binomio",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_6_cuadrado_binomio()