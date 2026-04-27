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
from mr_utils import evaluar_cumplimiento_mr, extraer_matriz, matrices_iguales
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_30_potencia_matriz():

    # Caso base:
    matriz = "[[1, 1], [0, 1]]"
    contexto = "Ten en cuenta que algunas matrices pueden escribirse como I + N, siendo N una matriz nilpotente (N^2 = 0), " \
               "lo que simplifica mucho el cálculo de potencias"
    prompt_base = (
        f"Calcula A^5 con A = {matriz}."
        "Responde SOLO con la matriz, sin texto adicional y en formato ASCII."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Calcula A^5 con A = {matriz}. {contexto}."
        "Responde SOLO con la matriz, sin texto adicional y en formato ASCII."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    matriz_base = extraer_matriz(respuesta_base)

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    matriz_transformada = extraer_matriz(respuesta_transformada)

    elapsed = time.perf_counter() - start

    cumple_mr = matrices_iguales(matriz_base, matriz_transformada)
    error_tecnico = False

    imprimir_resultados(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Calcular la potencia de la matriz {matriz}, sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Calcular la potencia de la matriz {matriz}, sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_30_potencia_matriz()