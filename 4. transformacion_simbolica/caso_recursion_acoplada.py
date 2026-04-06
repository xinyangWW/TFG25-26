import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_recursion_acoplada():
    prompt_base = """
    Dado el sistema de recurrencias acopladas:
    
    xₙ = 2xₙ₋₁ + yₙ₋₁
    yₙ = xₙ₋₁ + 2yₙ₋₁
    x₁ = 1, y₁ = 0
    
    Encuentra la forma cerrada para xₙ y yₙ.
    Responde solo con las expresiones separadas por coma (xₙ, yₙ).
    """
    
    prompt_transformado = """
    Calcula: xₙ = (3ⁿ + 1)/2, yₙ = (3ⁿ - 1)/2
    """

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base, respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Recursión sistema acoplado",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Recursión sistema acoplado",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_recursion_acoplada()