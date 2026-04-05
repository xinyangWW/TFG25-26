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
TIPO = "Relaciones funcionales"


def caso_11_orden_ramas_funcion_trozos():
    """
    MR: Reordenar las ramas de una función definida a trozos no altera su evaluación.
    f(x) = x^2 si x >= 0, -x si x < 0  →  misma función con ramas intercambiadas.
    Evaluamos f(-3). Resultado esperado: 3.
    """
    prompt_base = (
        "Sea f(x) definida a trozos: f(x) = x^2 si x >= 0, "
        "y f(x) = -x si x < 0. Calcula f(-3). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) definida a trozos: f(x) = -x si x < 0, "
        "y f(x) = x^2 si x >= 0. Calcula f(-3). "
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
        caso="Caso 11 Funcional: Orden de ramas en función a trozos — f(-3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 11 Funcional: Orden de ramas en función a trozos — f(-3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_11_orden_ramas_funcion_trozos()
