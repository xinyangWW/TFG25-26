import sys
import os
import math

sys.path.append(
    os.path.dirname(
        os.path.dirname(__file__)
    )
)
import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr, evaluar_integral_respuesta
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_26_integral_definida():

    # Caso base:
    expr = "abs(x)"
    a, b = -1, 1

    prompt_base = (
        f"Calcula la integral definida de {expr} desde {a} hasta {b}. "
        "Responde SOLO con un número, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    satisfy, error = evaluar_integral_respuesta(respuesta_base, expr, "x", a, b)

    prompt_transformado = (
        f"Comprueba si {respuesta_base} es el valor de la integral definida de {expr} entre {a} y {b}. "
        "Responde SI o NO, sin texto adicional."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    modelo_verifica = "si" in respuesta_transformada.lower()
    cumple_mr = (satisfy == modelo_verifica)
    error_tecnico = error

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la solución a la integral definida {expr} entre {a} y {b}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la solución a la integral definida {expr} entre {a} y {b}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_26_integral_definida()