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

def caso_suma_angulos(a: float, b: float):

    # Caso base:
    
    prompt_base = (
        f"Calcula sin({a} + {b}). "
        "Responde SOLO con un número, sin texto adicional."
    )

    # Caso transformado: 
    prompt_transformado = (
        f"Usa la fórmula del seno de la suma de angulos: "
        f"sin(a + b) = sin(a)cos(b) + cos(a)sin(b); para calcular sin({a} + {b}). "
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
        caso=f"Suma de ángulos ({a} + {b})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Generalización",
        caso=f"Suma de ángulos ({a} + {b})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_suma_angulos(30, 60)
    caso_suma_angulos(45, 45)
    caso_suma_angulos(123.5, 67.8)