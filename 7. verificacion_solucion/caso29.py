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
from mr_utils import extraer_matriz, multiplicar_matrices, matrices_iguales
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_29_producto_matrices():

    # Caso base:
    A = [[1, 2], [3, 4]]
    B = [[2, 0], [1, 2]]

    prompt_base = (
        f"Calcula el producto de las matrices A = {A} y B = {B}. "
        "Responde SOLO con la matriz resultado, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    matriz_modelo = extraer_matriz(respuesta_base)
    producto_matrices = multiplicar_matrices(A, B)

    satisfy = matrices_iguales(matriz_modelo, producto_matrices)

    matriz_str = respuesta_base.strip()

    prompt_transformado = (
        f"Comprueba si la matriz {matriz_str} es el resultado de multiplicar A={A} y B={B}. "
        "Responde SI o NO."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    modelo_verifica = "si" in respuesta_transformada.lower()
    error_tecnico = False

    cumple_mr = (satisfy == modelo_verifica)

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación del producto de matrices A={A} y B={B}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación del producto de matrices A={A} y B={B}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_29_producto_matrices()