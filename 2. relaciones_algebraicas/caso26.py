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


def caso_26_cuadrado_binomio(a_value: int, c_value: int):
    """
    MR: (x + a)^2 = c  es equivalente a  x^2 + 2ax + a^2 = c.
    Pedir la solución positiva para poder comparar con normalizar_respuesta.
    """
    double_a = 2 * a_value
    a_sq = a_value ** 2

    prompt_base = (
        f"Resuelve la ecuación: (x + {a_value})^2 = {c_value}. "
        "Indica solo la solución mayor de x. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la ecuación: x^2 + {double_a}x + {a_sq} = {c_value}. "
        "Indica solo la solución mayor de x. "
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
        caso=f"Caso 26: Cuadrado de binomio — (x+{a_value})^2={c_value} vs expandida, solución mayor",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 26: Cuadrado de binomio — (x+{a_value})^2={c_value} vs expandida, solución mayor",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_26_cuadrado_binomio(2, 25)   # (x+2)^2=25 → x=3
    caso_26_cuadrado_binomio(1, 16)   # (x+1)^2=16 → x=3
    caso_26_cuadrado_binomio(3, 36)   # (x+3)^2=36 → x=3
