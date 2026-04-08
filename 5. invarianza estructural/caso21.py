import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_21_teorema_convolucion():
    prompt_base = "Calcula la convolución de f(t)=e^(-t) y g(t)=e^(-2t) para t≥0, evaluada en t=2. Responde solo con el resultado numérico aproximado a 4 decimales."
    prompt_transformado = "Calcula: (e^(-2) - e^(-4)). Responde solo con el resultado numérico aproximado a 4 decimales."

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base, respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Invariancia estructural",
        caso="Caso 21: Teorema de convolución",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Invariancia estructural",
        caso="Caso 21: Teorema de convolución",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_21_teorema_convolucion()