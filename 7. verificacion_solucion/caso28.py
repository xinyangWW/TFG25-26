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
from mr_utils import evaluar_cumplimiento_mr, extraer_valores
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_28_numero_primo():

    # Caso base:
    N = 997
    prompt_base = (
        f"¿Es {N} un número primo? "
        "Responde SOLO con SI o NO, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    satisfy = "si" in respuesta_base.lower()

    prompt_transformado = (
        f"Lista los divisores de {N}. "
        "Responde SOLO con números, sin texto adicional."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    divisores = extraer_valores(respuesta_transformada)
    divisores = sorted(set(int(d) for d in divisores))

    if not divisores:
        modelo_verifica = False
    else: 

        todos_dividen = all(N % d == 0 for d in divisores if d != 0)
        modelo_verifica = todos_dividen and (1 in divisores) and (N in divisores) and len(divisores) == 2
        
    cumple_mr = (satisfy == modelo_verifica)
    error_tecnico = False

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la primalidad de {N}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la primalidad de {N}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_28_numero_primo()