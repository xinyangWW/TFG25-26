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


def caso_30_combinatorios_factoriales_potencias():
    prompt_base = (
        "Calcula el resultado de: (C(6,3) × 3! × 2^3) / (6! / 3!). Recuerda que C(n,k) = n!/(k!×(n-k)!) y que n! es el producto de todos los enteros positivos hasta n. Responde solo con el número o fracción simplificada, en español."
    )
    prompt_transformado = (
        "Calcula el resultado de: (20 × 6 × 8) / 120. Responde solo con el número o fracción simplificada, en español."
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
        caso="Caso 30: Expresión con combinatorios, factoriales y potencias (C(6,3)×3!×2^3 / (6!/3!) vs (20×6×8)/120)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 30: Expresión con combinatorios, factoriales y potencias (C(6,3)×3!×2^3 / (6!/3!) vs (20×6×8)/120)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_30_combinatorios_factoriales_potencias()
