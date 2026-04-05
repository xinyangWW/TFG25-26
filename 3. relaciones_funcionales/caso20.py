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


def caso_20_paridad_composicion():
    """
    MR: Si g(x) = f(x^2) y f es cualquier función, entonces g es siempre par:
    g(x) = g(-x), ya que x^2 = (-x)^2.
    f(x) = 3x + 1, g(x) = f(x^2) = 3x^2 + 1.
    g(4) debe coincidir con g(-4). Resultado esperado: 49.
    """
    prompt_base = (
        "Sea f(x) = 3x + 1 y g(x) = f(x^2). Calcula g(4). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = 3x + 1 y g(x) = f(x^2). Calcula g(-4). "
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
        caso="Caso 20 Funcional: Paridad por composición — g(4) vs g(-4) con g(x)=f(x^2)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 20 Funcional: Paridad por composición — g(4) vs g(-4) con g(x)=f(x^2)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_20_paridad_composicion()
