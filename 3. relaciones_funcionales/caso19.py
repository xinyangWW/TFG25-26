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


def caso_19_cuadratica_estandar_vs_factorizada():
    """
    MR: La forma estándar y la forma factorizada de un polinomio son equivalentes.
    f(x) = x^2 - 5x + 6  →  g(x) = (x - 2)(x - 3).
    Evaluamos en x = 7. Resultado esperado: 12.
    """
    prompt_base = (
        "Sea f(x) = x^2 - 5x + 6. Calcula f(7). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea g(x) = (x - 2)(x - 3). Calcula g(7). "
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
        caso="Caso 19 Funcional: Cuadrática estándar vs factorizada — f(7)=x^2-5x+6 vs g(7)=(x-2)(x-3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 19 Funcional: Cuadrática estándar vs factorizada — f(7)=x^2-5x+6 vs g(7)=(x-2)(x-3)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_19_cuadratica_estandar_vs_factorizada()
