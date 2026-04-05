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


def caso_18_inecuacion_reescrita():
    """
    MR: Reescribir una inecuación pasando términos al otro lado produce
    una inecuación equivalente con la misma solución.
    4x - 3 > 2x + 7  →  4x - 2x > 7 + 3  →  2x > 10  →  x > 5.
    Pedimos el valor entero mínimo que satisface la inecuación.
    Resultado esperado: 6.
    """
    prompt_base = (
        "Resuelve la inecuación: 4x - 3 > 2x + 7. Indica el valor entero mínimo de x que satisface la inecuación. Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Resuelve la inecuación: 2x > 10. Indica el valor entero mínimo de x que satisface la inecuación. Responde solo con la respuesta, en español."
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
        caso="Caso 18: Inecuación reescrita (4x-3>2x+7 vs 2x>10)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 18: Inecuación reescrita (4x-3>2x+7 vs 2x>10)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_18_inecuacion_reescrita()
