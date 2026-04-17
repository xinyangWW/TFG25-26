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

def caso_16_suma_telescopica(n: int):

    # Caso base: 
    terminos = [f"1/({i}({i} + 1))" for i in range(1, n + 1)]
    suma_explicitada = " + ".join(map(str, terminos))
    
    prompt_base = (
        f"Calcula la siguiente suma: {suma_explicitada}. "
        "Responde SOLO con un número, sin texto adicional."
    )

    # Caso transformado:
    prompt_transformado = (
        f"Usa la fórmula de la suma telescopica: S(n) = 1 - 1/(n + 1); y calcula la suma de 1 hasta {n}. "
        "Responde SOLO con un número, sin texto adicional."
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
        caso=f"Suma telescopica (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Suma telescopica (n={n})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_16_suma_telescopica(11)