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

def caso_23_suma_diferencias_cubicas(n: int):

    terminos = [f"({k}^3 - {k-1}^3)" for k in range(2, n+1)]
    suma_explicitada = " + ".join(map(str, terminos))
    
    prompt_base = (
        f"Calcula la suma: {suma_explicitada}. "
        "Responde SOLO con un número, sin texto adicional."
    )

    prompt_transformado = (
        f"Usa la fórmula sum(k^3 - (k-1)^3) = n^3 - 1 con n = {n}. "
        "Responde SOLO con un número, sin texto adicional."
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
        caso=f"Suma de diferencias cúbicas (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Suma de diferencias cúbicas (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_23_suma_diferencias_cubicas(7)