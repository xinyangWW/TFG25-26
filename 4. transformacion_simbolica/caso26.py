import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_26_criptoaritmetica():
    prompt_base = """
    Resuelve la criptoaritmética:
    
      S E N D
    + M O R E
    ---------
    M O N E Y
    
    Cada letra representa un dígito único (0-9). M ≠ 0.
    
    ¿Qué valores tienen S, E, N, D, M, O, R, Y?
    Responde con: S,E,N,D,M,O,R,Y en ese orden separados por comas.
    """
    
    prompt_transformado = """
    Calcula: 9,5,6,7,1,0,8,2
    (Verificación: 9567 + 1085 = 10652)
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
        tipo="Razonamiento simbólico",
        caso="Caso 26: Criptoaritmética SEND+MORE",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Razonamiento simbólico",
        caso="Caso 26: Criptoaritmética SEND+MORE",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_26_criptoaritmetica()