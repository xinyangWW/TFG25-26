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

def caso_25_opti_2a_derivada():

    # Caso base:
    funcion = "x^3 - 3x^2 + 2"
    contexto = "ten en cuenta que un punto crítico es mínimo si f''(x) > 0 y máximo si f''(x) < 0"
    prompt_base = (
        f"Encuentra el mínimo de la función {funcion}."
        "Responde SOLO con el valor de x, sin texto adicional y en formato ASCII."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Encuentra el mínimo de la función {funcion}, {contexto}."
        "Responde SOLO con el valor de x, sin texto adicional y en formato ASCII."
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
        tipo="Contexto Previo",
        caso=f"Calcular el mínimo de la función {funcion}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Calcular el mínimo de la función {funcion}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_25_opti_2a_derivada()