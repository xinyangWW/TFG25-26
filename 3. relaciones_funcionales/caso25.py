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


def caso_25_cambio_base_logaritmo():
    """
    MR: Fórmula de cambio de base: log_b(x) = log_c(x) / log_c(b).
    log_4(64) = log_2(64) / log_2(4) = 6 / 2 = 3.
    Evaluamos log_4(64) directamente y mediante cambio de base en base 2.
    Resultado esperado: 3.
    """
    prompt_base = (
        "Calcula log en base 4 de 64, es decir, ¿a qué potencia hay que elevar 4 para obtener 64? "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Calcula log en base 2 de 64 dividido entre log en base 2 de 4, "
        "es decir, log2(64) / log2(4). "
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
        caso="Caso 25 Funcional: Cambio de base — log4(64) vs log2(64)/log2(4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 25 Funcional: Cambio de base — log4(64) vs log2(64)/log2(4)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_25_cambio_base_logaritmo()
