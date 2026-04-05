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


def caso_22_formula_general_vs_factorizacion(c_value: int):
    """
    MR: Resolver x^2 - c = 0 mediante la fórmula general o por raíz cuadrada
    debe dar la misma solución positiva.
    x = sqrt(c).
    """
    prompt_base = (
        f"Resuelve la ecuación x^2 - {c_value} = 0 usando la fórmula general. "
        "Indica solo la solución positiva. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación x^2 = {c_value} calculando la raíz cuadrada. "
        "Indica solo la solución positiva. "
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
        caso=f"Caso 22: Fórmula general vs raíz cuadrada (c = {c_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 22: Fórmula general vs raíz cuadrada (c = {c_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_22_formula_general_vs_factorizacion(9)
    caso_22_formula_general_vs_factorizacion(25)
    caso_22_formula_general_vs_factorizacion(49)
