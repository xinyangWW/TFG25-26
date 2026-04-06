import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_recursion_alternada():
    prompt_base = """
    Dada la definición recursiva por partes:
    
    a₁ = 1
    a₂ = 3
    aₙ = 2·aₙ₋₁ + 3·aₙ₋₂  si n es impar
    aₙ = aₙ₋₁ + 2·aₙ₋₂    si n es par
    
    Encuentra la forma cerrada para aₙ.
    Responde solo con la expresión en términos de n.
    """
    
    prompt_transformado = """
    Calcula: aₙ = 2ⁿ - (-1)ⁿ (para n impar: 2ⁿ - 1, para n par: 2ⁿ + 1)
    O más compacto: aₙ = 2ⁿ + (-1)ⁿ⁺¹
    """

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base, respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Recursión alternada por paridad",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Recursión alternada por paridad",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_recursion_alternada()