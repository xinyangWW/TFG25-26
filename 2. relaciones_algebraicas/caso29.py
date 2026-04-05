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


def caso_29_inecuacion_escalada(k_value: int):
    """
    MR: Multiplicar ambos miembros de una inecuación por k > 0 no altera
    el sentido ni la solución.
    x > 3  →  kx > 3k.
    Pedimos el entero mínimo que satisface la inecuación. Resultado esperado: 4.
    """
    rhs = 3 * k_value

    prompt_base = (
        "Resuelve la inecuación: x > 3. "
        "Indica el valor entero mínimo de x que la satisface. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        f"Resuelve la inecuación: {k_value}x > {rhs}. "
        "Indica el valor entero mínimo de x que la satisface. "
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
        caso=f"Caso 29: Inecuación escalada por k={k_value} — x>3 vs {k_value}x>{rhs}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso=f"Caso 29: Inecuación escalada por k={k_value} — x>3 vs {k_value}x>{rhs}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_29_inecuacion_escalada(2)
    caso_29_inecuacion_escalada(5)
    caso_29_inecuacion_escalada(10)
