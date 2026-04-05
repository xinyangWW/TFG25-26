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


def caso_28_fracciones_mcm(num: int, den: int, rhs: int):
    """
    MR: x/den = rhs/num  es equivalente a  num*x = den*rhs  tras multiplicar
    ambos miembros por den*num (MCM cuando son coprimos).
    Resultado esperado: x = (den * rhs) / num.
    """
    lhs_expanded = den * rhs

    prompt_base = (
        f"Resuelve la ecuación: x / {den} = {rhs} / {num}. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación: {num}x = {lhs_expanded}. "
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
        caso=f"Caso 28: Fracciones con MCM — x/{den}={rhs}/{num} vs {num}x={lhs_expanded}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 28: Fracciones con MCM — x/{den}={rhs}/{num} vs {num}x={lhs_expanded}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_28_fracciones_mcm(3, 4, 6)    # x/4 = 6/3 → x = 8
    caso_28_fracciones_mcm(5, 2, 10)   # x/2 = 10/5 → x = 4
    caso_28_fracciones_mcm(2, 6, 9)    # x/6 = 9/2 → x = 27
