import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_15_probabilidad_condicional():
    prompt_base = "En una población, el 1% tiene una enfermedad. Una prueba detecta el 99% de los casos y da 20% falsos positivos. Si alguien da positivo, ¿probabilidad de estar enfermo? Responde solo con el porcentaje."
    prompt_transformado = "Calcula: (0.01*0.99)/(0.01*0.99+0.99*0.20)*100. Responde solo con el porcentaje."

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base, respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Invariancia estructural",
        caso="Caso 15: Teorema de Bayes",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Invariancia estructural",
        caso="Caso 15: Teorema de Bayes",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_15_probabilidad_condicional()