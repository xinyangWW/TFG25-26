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

def caso_24_integral():

    # Caso base:
    funcion = "e^(-x)"
    contexto = "ten en cuenta que la integral converge y se puede calcular como un límite"
    prompt_base = (
        f"Calcula la integral de {funcion} entre 0 e infinito."
        "Responde SOLO con un número, sin texto adicional y en formato ASCII."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Calcula la integral de {funcion} entre 0 e infinito, {contexto}."
        "Responde SOLO con un número, sin texto adicional y en formato ASCII."
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
        caso=f"Calcular la integral de {funcion} entre 0 e infinito; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Calcular la integral de {funcion} entre 0 e infinito; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_24_integral()