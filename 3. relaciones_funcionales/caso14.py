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


def caso_14_composicion_tres_funciones():
    """
    MR: La composición de tres funciones evaluada paso a paso debe coincidir
    con la fórmula directa resultante de sustituir.
    f(x) = 2x, g(x) = x + 3, h(x) = x^2.
    h(g(f(1))) = h(g(2)) = h(5) = 25.
    Formulación base: paso a paso.
    Formulación transformada: fórmula directa (2x+3)^2 evaluada en x=1.
    Resultado esperado: 25.
    """
    prompt_base = (
        "Sea f(x) = 2x, g(x) = x + 3 y h(x) = x^2. "
        "Calcula h(g(f(1))). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea p(x) = (2x + 3)^2. Calcula p(1). "
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
        caso="Caso 14: Composición de tres funciones — h(g(f(1))) vs p(1)=(2x+3)^2",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 14: Composición de tres funciones — h(g(f(1))) vs p(1)=(2x+3)^2",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_14_composicion_tres_funciones()
