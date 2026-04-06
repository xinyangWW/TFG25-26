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
TIPO = "Aritmética"


def caso_26_triple_producto_raices_telescopico():
    """
    MR: El producto de raíces encadenadas puede reagruparse dentro de una única
    raíz utilizando la propiedad multiplicativa de la raíz cuadrada.
    sqrt(2/3) × sqrt(3/5) × sqrt(5/7) × sqrt(7/2)
    → sqrt((2/3) × (3/5) × (5/7) × (7/2)).
    Resultado esperado: 1.
    """
    prompt_base = (
        "Calcula el resultado de: sqrt(2/3) × sqrt(3/5) × sqrt(5/7) × sqrt(7/2). Responde solo con la respuesta, en español. "
    )
    prompt_transformado = (
        "Calcula el resultado de: sqrt((2/3) × (3/5) × (5/7) × (7/2)). Responde solo con la respuesta, en español. "
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
        caso="Caso 26: Producto telescópico de raíces (sqrt(2/3)×sqrt(3/5)×sqrt(5/7)×sqrt(7/2) vs 1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 26: Producto telescópico de raíces (sqrt(2/3)×sqrt(3/5)×sqrt(5/7)×sqrt(7/2) vs 1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_26_triple_producto_raices_telescopico()
