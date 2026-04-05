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


def caso_2_distribucion_con_excepcion(a_value: int):
    """
    MR: Aplicar la propiedad distributiva no cambia la solución,
    salvo cuando el parámetro hace degenerar la ecuación.
    a(x + 2) = ax + 4 → ax + 2a = ax + 4.
    Resultado esperado: para a ≠ 0, la ecuación conserva su solución;
    para a = 0, aparece un caso excepcional.
    """
    prompt_base = (
        f"Para a = {a_value}, resuelve: a(x + 2) = ax + 4. "
        "Responde solo con la solución, en español."
    )

    prompt_transformado = (
        f"Para a = {a_value}, resuelve: ax + 2a = ax + 4. "
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
        caso=f"Caso 2: Distribución con excepción (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 2: Distribución con excepción (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)

    caso_2_distribucion_con_excepcion(2)
    caso_2_distribucion_con_excepcion(0)