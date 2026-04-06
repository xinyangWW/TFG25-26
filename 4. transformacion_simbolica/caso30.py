import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_30_maquina_turing():
    prompt_base = """
    Máquina de Turing con cinta inicial: ... 0 1 1 0 1 ...
    Reglas:
    - Estado q0: leer 0 → escribe 1, mueve derecha, va a q1
    - Estado q0: leer 1 → escribe 0, mueve derecha, va a q0
    - Estado q1: leer 0 → escribe 0, mueve izquierda, va a q0
    - Estado q1: leer 1 → escribe 1, mueve derecha, va a q1
    
    Estado inicial: q0, posición: en el primer 1
    Cinta: [0] 1 1 0 1 (el primer símbolo es 0)
    
    ¿Cuál es el estado de la cinta después de 3 pasos?
    Responde con la secuencia de 5 símbolos.
    """
    
    prompt_transformado = """
    Calcula: 1,0,1,0,1
    (Explicación: 
     Paso1: leer 0, escribe 1→ q1: cinta 1,1,1,0,1
     Paso2: leer 1, escribe 1, mueve derecha→ q1: cinta 1,1,1,0,1
     Paso3: leer 1, escribe 1, mueve derecha→ q1: cinta 1,1,1,0,1)
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
        caso="Caso 30: Máquina Turing",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Razonamiento simbólico",
        caso="Caso 30: Máquina Turing",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_30_maquina_turing()