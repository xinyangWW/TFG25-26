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


def caso_3_factor_comun_con_excepcion(a_value: int):
    """
    MR: Expandir una ecuación con factor común no cambia la solución,
    salvo cuando el factor común se anula.
    (a - 3)(x - 2) = (a - 3)(x + 1)
    → (a - 3)x - 2(a - 3) = (a - 3)x + (a - 3).
    Resultado esperado: para a ≠ 3, no hay solución;
    para a = 3, aparece un caso excepcional.
    """
    prompt_base = (
        f"Para a = {a_value}, resuelve: (a - 3)(x - 2) = (a - 3)(x + 1). "
        "Responde solo con la solución, en español."
    )

    prompt_transformado = (
        f"Para a = {a_value}, resuelve: "
        f"(a - 3)x - 2(a - 3) = (a - 3)x + (a - 3). "
        "Responde solo con la solución, en español."
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
        caso=f"Caso 3: Factor común con excepción (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 3: Factor común con excepción (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)

    caso_3_factor_comun_con_excepcion(5)
    caso_3_factor_comun_con_excepcion(3)