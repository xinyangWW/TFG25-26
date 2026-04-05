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


def caso_23_distributiva(a_value: int, b_value: int, c_value: int):
    """
    MR: La forma factorizada a(x + b) = c y la forma expandida ax + ab = c
    deben dar la misma solución.
    """
    ab = a_value * b_value

    prompt_base = (
        f"Resuelve la ecuación: {a_value}(x + {b_value}) = {c_value}. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación: {a_value}x + {ab} = {c_value}. "
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
        caso=f"Caso 23: Distributiva — {a_value}(x+{b_value})={c_value} vs {a_value}x+{ab}={c_value}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 23: Distributiva — {a_value}(x+{b_value})={c_value} vs {a_value}x+{ab}={c_value}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_23_distributiva(3, 4, 21)
    caso_23_distributiva(5, 2, 30)
    caso_23_distributiva(2, 7, 20)
