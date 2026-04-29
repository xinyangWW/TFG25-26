import sys
import os
import random

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

def caso_15_integral_polinomio(n: int):

    terminos = [f"{random.randint(1,9)}{'x^' + str(i) if i > 0 else ''}" for i in range(n, -1, -1)]
    polinomio = " + ".join(map(str, terminos))
    # Caso base
    
    prompt_base = (
        f"Calcula la integral de {polinomio}. "
        "Responde SOLO la integral, sin texto adicional y en formato ASCII."
    )

    # Caso transformado: fórmula general
    prompt_transformado = (
        f"Usa la fórmula de la integral de x^n = x^(n+1)/(n+1), e integra {polinomio}. "
        "Responde SOLO la integral, sin texto adicional y en formato ASCII."
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

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Integral de {polinomio}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Integral de {polinomio}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_15_integral_polinomio(5)
