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

def caso_binomio_newton(a: int, b: int, n: int):

    # Caso base:
    
    prompt_base = (
        f"Calcula la siguiente suma ({a} + {b})^{n}. "
        "Responde SOLO con un número, sin texto adicional."
    )

    # Caso transformado: 
    prompt_transformado = (
        f"Usa la fórmula del binomio de Newton: "
        "(a + b)^n = sum_{k=0}^n C(n,k) a^(n-k) b^k; para calcular ({a} + {b})^{n}. "
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
        caso=f"Binomio de Newton ({a} + {b})^{n}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Binomio de Newton ({a} + {b})^{n}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_binomio_newton(2, 3, 4)
    caso_binomio_newton(1, 1, 5) 
    caso_binomio_newton(-2, 5, 7)