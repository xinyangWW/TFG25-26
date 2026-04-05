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


def caso_25_variable_ambos_lados(a_value: int, b_value: int, c_value: int):
    """
    MR: ax = bx + c  es equivalente a  (a-b)x = c tras agrupar la variable.
    """
    diff = a_value - b_value

    prompt_base = (
        f"Resuelve la ecuación: {a_value}x = {b_value}x + {c_value}. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación: {diff}x = {c_value}. "
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
        caso=f"Caso 25: Variable en ambos lados — {a_value}x={b_value}x+{c_value} vs {diff}x={c_value}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 25: Variable en ambos lados — {a_value}x={b_value}x+{c_value} vs {diff}x={c_value}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_25_variable_ambos_lados(7, 3, 12)
    caso_25_variable_ambos_lados(9, 4, 20)
    caso_25_variable_ambos_lados(6, 2, 16)
