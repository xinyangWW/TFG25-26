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

def caso_11_derivada_regla_cadena():

    # Caso base:
    expr = "sin(x^2)"
    contexto = "recuerda la regla de la cadena: f(g(x))' = f'(g(x)) * g'(x)"
    prompt_base = (
        f"Calcula la derivada de {expr}."
        "Responde SOLO con la derivada, sin texto adicional y en formato ASCII."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Calcula la derivada de {expr}, {contexto}."
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
        caso=f"Calcular la derivada de {expr}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Calcular la derivada de {expr}; sin y con el contexto: {contexto}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_11_derivada_regla_cadena()