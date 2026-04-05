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
TIPO = "Algebraica"


def caso_27_sistema_multiplos(k_value: int):
    """
    MR: Multiplicar todas las ecuaciones de un sistema por una constante k
    no altera la solución.
    Sistema base: x + y = 6, x - y = 2  →  x = 4.
    Sistema transformado: kx + ky = 6k, kx - ky = 2k  →  x = 4.
    """
    s1 = 6 * k_value
    s2 = 2 * k_value

    prompt_base = (
        "Resuelve el sistema: x + y = 6 y x - y = 2. "
        "Indica solo el valor de x. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve el sistema: {k_value}x + {k_value}y = {s1} y "
        f"{k_value}x - {k_value}y = {s2}. "
        "Indica solo el valor de x. "
        "Responde solo con la respuesta, en español."
    )

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 27: Sistema escalado por k={k_value} — solución de x invariante",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 27: Sistema escalado por k={k_value} — solución de x invariante",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_27_sistema_multiplos(2)
    caso_27_sistema_multiplos(3)
    caso_27_sistema_multiplos(5)
