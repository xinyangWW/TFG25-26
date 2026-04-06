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


def caso_7_telescopica_vs_directa():
    """
    MR: Una suma telescópica puede simplificarse a su resultado cerrado.
    Cada término 1/(n×(n+1)) = 1/n - 1/(n+1), por lo que los términos
    intermedios se cancelan y la suma total es 1 - 1/5 = 4/5.
    1/(1×2) + 1/(2×3) + 1/(3×4) + 1/(4×5)  →  4/5.
    Resultado esperado: 0.8.
    """
    prompt_base = (
        "Calcula el resultado de: 1/(1×2) + 1/(2×3) + 1/(3×4) + 1/(4×5). Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Calcula el resultado de: 4/5. Responde solo con la respuesta, en español."
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
        caso="Caso 7: Suma telescópica vs resultado directo (1/(1×2)+1/(2×3)+1/(3×4)+1/(4×5) vs 4/5)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 7: Suma telescópica vs resultado directo (1/(1×2)+1/(2×3)+1/(3×4)+1/(4×5) vs 4/5)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_7_telescopica_vs_directa()
