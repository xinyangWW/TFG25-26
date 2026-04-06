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
TIPO = "Aritmética"


def caso_27_suma_fracciones_cubo_equivalente():
    """
    MR: Si una expresión algebraica puede simplificarse a un valor numérico
    exacto, elevar esa expresión o su valor equivalente a una potencia no
    altera el resultado final.

    (1/2 + 1/3 + 1/6) = 1
    (1/2 + 1/3 + 1/6)^3  →  1^3

    Resultado esperado: 1.
    """

    prompt_base = (
        "Calcula el resultado de: (1/2 + 1/3 + 1/6)^3. "
        "Responde solo con la respuesta, en español. "
    )

    prompt_transformado = (
        "Calcula el resultado de: 1^3. "
        "Responde solo con la respuesta, en español. "
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
        caso="Caso 27: Simplificación de suma de fracciones antes de potencia ((1/2+1/3+1/6)^3 vs 1^3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 27: Simplificación de suma de fracciones antes de potencia ((1/2+1/3+1/6)^3 vs 1^3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_27_suma_fracciones_cubo_equivalente()

