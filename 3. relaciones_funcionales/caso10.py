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


def caso_10_exponencial_verbal_vs_formula():
    """
    MR: Describir una función exponencial en lenguaje natural o como fórmula
    debe producir el mismo resultado al evaluarla.
    "Una cantidad que se duplica cada paso, empezando en 1, tras 4 pasos"
    equivale a f(x) = 2^x evaluada en x=4.
    Resultado esperado: 16.
    """
    prompt_base = (
        "Sea f(x) = 2^x. Calcula f(4). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Una cantidad empieza en 1 y se duplica en cada paso. "
        "¿Cuánto vale después de 4 pasos? "
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
        caso="Caso 10: Exponencial — f(4)=2^x vs descripción verbal de duplicación",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 10: Exponencial — f(4)=2^x vs descripción verbal de duplicación",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_10_exponencial_verbal_vs_formula()
