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


def caso_21_logaritmo_producto_suma():
    """
    MR: Propiedad del logaritmo log(a·b) = log(a) + log(b).
    log2(4 · 8) debe coincidir con log2(4) + log2(8).
    log2(32) = 5, log2(4) + log2(8) = 2 + 3 = 5.
    Resultado esperado: 5.
    """
    prompt_base = (
        "Calcula log en base 2 de 32, es decir, log2(32). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Calcula log en base 2 de 4 más log en base 2 de 8, "
        "es decir, log2(4) + log2(8). "
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
        caso="Caso 21 Funcional: Logaritmo de producto — log2(32) vs log2(4)+log2(8)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 21 Funcional: Logaritmo de producto — log2(32) vs log2(4)+log2(8)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_21_logaritmo_producto_suma()
