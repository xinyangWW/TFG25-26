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


def caso_10_parametro_cancelacion(a_value: int):
    """
    MR: Desarrollar una ecuación con un factor paramétrico no cambia la solución,
    salvo cuando dicho factor se anula.
    (a + 1)(x - 2) = 0 → (a + 1)x - 2(a + 1) = 0.
    Resultado esperado: para a ≠ -1, x = 2;
    para a = -1, aparece un caso excepcional.
    """
    prompt_base = (
        f"Para a = {a_value}, resuelve la ecuación: "
        f"(a + 1)(x - 2) = 0. "
        "Responde solo con la solución, en español."
    )

    prompt_transformado = (
        f"Para a = {a_value}, resuelve la ecuación: "
        f"(a + 1)x - 2(a + 1) = 0. "
        "Responde solo con la solución, en español."
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
        tipo=TIPO,
        caso=f"Caso 10: Cancelación con parámetro (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 10: Cancelación con parámetro (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)

    caso_10_parametro_cancelacion(2)
    caso_10_parametro_cancelacion(-1)