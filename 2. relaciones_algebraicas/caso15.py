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
TIPO = "Algebraica"


def caso_15_cuadratica_completar_cuadrado():
    """
    MR: Una ecuación cuadrática resuelta en forma estándar y mediante
    completar el cuadrado deben dar las mismas soluciones.
    x^2 + 6x + 5 = 0  →  (x + 3)^2 = 4.
    Soluciones: x = -1 y x = -5.
    Pedimos la solución mayor para poder comparar con normalizar_respuesta.
    Resultado esperado: -1.
    """
    prompt_base = (
        "Resuelve la ecuación x^2 + 6x + 5 = 0. Indica solo el valor mayor de x entre las dos soluciones. Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Resuelve la ecuación (x + 3)^2 = 4. Indica solo el valor mayor de x entre las dos soluciones. Responde solo con la respuesta, en español."
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
        caso="Caso 15: Cuadrática completar cuadrado (x^2+6x+5=0 vs (x+3)^2=4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 15: Cuadrática completar cuadrado (x^2+6x+5=0 vs (x+3)^2=4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_15_cuadratica_completar_cuadrado()