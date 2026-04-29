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
from mr_utils import es_matriz_identidad, extraer_matriz, multiplicar_matrices, matrices_iguales
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_32_matriz_inversa3x3():

    # Caso base:
    A = [
        [1, 2, 3],
        [0, 1, 4],
        [5, 6, 0]
    ]

    prompt_base = (
        f"Calcula la matriz inversa de A = {A}. "
        "Responde SOLO con la matriz resultado, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    matriz_inversa = extraer_matriz(respuesta_base)

    if not matriz_inversa:
        satisfy = False
        error = True
    else:
        producto = multiplicar_matrices(A, matriz_inversa)
        satisfy = es_matriz_identidad(producto)
        error = False

    prompt_transformado = (
        f"Comprueba si la matriz {respuesta_base} es la matriz inversa de A={A}. "
        "Responde SI o NO."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    modelo_verifica = "si" in respuesta_transformada.lower()
    error_tecnico = error
    cumple_mr = (satisfy == modelo_verifica)

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la matriz inversa de A={A}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la matriz inversa de A={A}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_32_matriz_inversa3x3()