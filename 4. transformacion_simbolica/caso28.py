import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_28_teoria_juegos():
    prompt_base = """
    En el dilema del prisionero iterado con estrategia "Tit for Tat" (cooperar en primera ronda,
    luego copiar la acción del oponente en la ronda anterior):
    
    Si el oponente juega: C, D, C, C, D (C=Cooperar, D=Defectar)
    ¿Cuál es la secuencia de jugadas de "Tit for Tat"?
    
    Responde solo con la secuencia separada por comas.
    """
    
    prompt_transformado = """
    Calcula: C, C, D, C, C
    (Explicación: Ronda1: C, Ronda2: copia oponente ronda1=C, Ronda3: copia oponente ronda2=D,
    Ronda4: copia oponente ronda3=C, Ronda5: copia oponente ronda4=C)
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
        caso="Caso 28: Teoría juegos Tit for Tat",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Razonamiento simbólico",
        caso="Caso 28: Teoría juegos Tit for Tat",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_28_teoria_juegos()