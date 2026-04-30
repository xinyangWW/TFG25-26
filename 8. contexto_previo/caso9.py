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
from mr_utils import evaluar_cumplimiento_expresiones
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_9_derivada_regla_producto():

    # Caso base:
    expr = "x^2 * e^x"
    contexto = "mediante la regla del producto (fg)' = f'g + fg'"
    prompt_base = (
        f"Deriva: {expr}."
        "Responde SOLO con la derivada, sin texto adicional y en formato ASCII."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Deriva {expr} {contexto}."
        "Responde SOLO con la derivada, sin texto adicional y en formato ASCII."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_expresiones(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Derivar la función {expr}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Derivar la función {expr}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_9_derivada_regla_producto()