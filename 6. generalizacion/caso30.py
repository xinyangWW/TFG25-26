import sys
import os
import math

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

def caso_30_aprox_taylor(n: int):

    
    terminos = ["1"] + [f"1/{math.factorial(i)}" for i in range(1, n + 1)]
    suma_explicitada = " + ".join(terminos)
    
    # Caso base: 
    prompt_base = (
        f"Calcula el valor numérico de la siguiente suma: {suma_explicitada}. "
        "Responde SOLO con el número decimal."
    )

    # Caso transformado: 
    prompt_transformado = (
        f"Calcula la suma 1/0! + 1/1! + 1/2! + ... + 1/{n}!. "
        "Responde SOLO con un número decimal."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Aproximación por series de Taylor",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Aproximación por series de Taylor",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_30_aprox_taylor(9)