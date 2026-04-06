import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_sucesion_collatz():
    prompt_base = """
    La conjetura de Collatz (3n+1): Para cualquier número entero positivo n, 
    la siguiente sucesión eventualmente llega a 1:
    - Si n es par: n → n/2
    - Si n es impar: n → 3n+1
    
    Para n = 27, calcula:
    1. ¿Cuántos pasos tarda en llegar a 1?
    2. ¿Cuál es el valor máximo alcanzado durante la sucesión?
    
    Responde con: pasos, maximo
    """
    
    prompt_transformado = """
    Calcula: 111, 9232
    (La sucesión de 27 tiene 111 pasos y alcanza un máximo de 9232)
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
        caso="Conjetura Collatz n=27",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Conjetura Collatz n=27",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_sucesion_collatz()