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

def caso_21_suma_cuadrados(n: int):

    # Caso base:
    terminos = [f"{i}^2" for i in range(1, n + 1)]
    suma_explicitada = " + ".join(map(str, terminos))
    
    prompt_base = (
        f"Calcula la siguiente suma de cuadrados: {suma_explicitada}. "
        "Responde SOLO con un número entero, sin texto adicional."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Usa la fórmula de la suma de cuadrados de los primeros n números naturales S(n) = n * (n + 1) * (2n + 1) / 6, con n={n}. "
        "Responde SOLO con un número entero, sin texto adicional."
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
        caso=f"Suma de cuadrados (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Suma de cuadrados (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_21_suma_cuadrados(7)