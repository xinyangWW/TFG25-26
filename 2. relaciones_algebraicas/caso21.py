
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


def caso_21_valor_absoluto():
    """
    MR: Resolver una ecuación con valor absoluto o como dos ecuaciones lineales produce las mismas soluciones.
    """

    prompt_base = (
        "Resuelve la ecuación: |x - 4| = 6. Responde solo con las soluciones, en español. "
    )

    prompt_transformado = (
        "Resuelve las ecuaciones: x - 4 = 6 y x - 4 = -6. Responde solo con las soluciones, en español. "
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
        caso="Caso 21: Ecuación con valor absoluto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformado,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 21: Ecuación con valor absoluto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformado,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_21_valor_absoluto()
