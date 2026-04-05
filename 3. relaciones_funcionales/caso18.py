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


def caso_18_exponencial_suma_producto():
    """
    MR: Para f(x) = 2^x se cumple f(a + b) = f(a) · f(b).
    Evaluamos f(3 + 2) = f(5) = 32 directamente
    y también f(3) · f(2) = 8 · 4 = 32.
    Resultado esperado: 32.
    """
    prompt_base = (
        "Sea f(x) = 2^x. Calcula f(5). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = 2^x. Calcula f(3) multiplicado por f(2). "
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
        caso="Caso 18 Funcional: Propiedad exponencial — f(5)=2^5 vs f(3)·f(2)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 18 Funcional: Propiedad exponencial — f(5)=2^5 vs f(3)·f(2)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_18_exponencial_suma_producto()
