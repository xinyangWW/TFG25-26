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
from mr_utils import evaluar_extremo_global, extraer_valores
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_33_extremos_funcion():

    # Caso base:
    funcion = "-x^2 + 4*x"

    prompt_base = (
        f"Calcula el valor donde la función {funcion} alcanza su máximo global. "
        "Responde SOLO con el valor de x, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    satisfy, error = evaluar_extremo_global(respuesta_base, funcion)

    prompt_transformado = (
        f"Comprueba si x = {respuesta_base} es el máximo global de la función {funcion}. "
        "Responde SI o NO, sin texto adicional."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    modelo_verifica = "si" in respuesta_transformada.lower()
    error_tecnico = error
    cumple_mr = satisfy and modelo_verifica

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación del máximo global de la función {funcion}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación del máximo global de la función {funcion}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_33_extremos_funcion()