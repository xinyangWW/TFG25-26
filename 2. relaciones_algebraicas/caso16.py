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


def caso_16_sistema_sustitucion_vs_eliminacion():
    """
    MR: Resolver un sistema de ecuaciones por sustitución o por eliminación
    debe dar el mismo valor de x.
    Sistema: x + y = 10, x - y = 4.
    Solución: x = 7, y = 3. Pedimos solo x.
    Resultado esperado: x = 7.
    """
    prompt_base = (
        "Resuelve el siguiente sistema de ecuaciones usando el método de sustitución: x + y = 10 y x - y = 4. Indica solo el valor de x. Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Resuelve el siguiente sistema de ecuaciones sumando ambas ecuaciones: x + y = 10 y x - y = 4. Indica solo el valor de x. Responde solo con la respuesta, en español."
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
        caso="Caso 16: Sistema sustitución vs eliminación (x+y=10 y x-y=4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 16: Sistema sustitución vs eliminación (x+y=10 y x-y=4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_16_sistema_sustitucion_vs_eliminacion()
