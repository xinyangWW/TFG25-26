import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import time
from query_model import query_model, preload_model
from results_manager import guardar_resultado
from mr_utils import evaluar_cumplimiento_mr
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemma:2b"


def caso_silogismo_avanzado():
    prompt_base = """
    Dadas las siguientes premisas:
    
    1. Todos los lógicos son matemáticos.
    2. Ningún matemático es ignorante.
    3. Algunos filósofos son lógicos.
    4. Todos los ignorantes son analfabetos funcionales.
    5. Quienes no son matemáticos, o son físicos o son químicos.
    6. Ningún químico es filósofo.
    7. Todos los físicos son científicos.
    8. Los analfabetos funcionales no pueden ser científicos.
    
    Pregunta: ¿Se puede deducir que algún filósofo no es químico? 
    ¿Y que algún filósofo es científico?
    
    Responde con "Sí" o "No" para cada pregunta, separados por coma.
    Ejemplo: Sí, No
    """
    
    prompt_transformado = """
    Calcula: Sí, No (porque los filósofos que son lógicos son matemáticos, 
    los matemáticos no son ignorantes, y los no ignorantes pueden ser científicos;
    pero ningún químico es filósofo, por lo tanto algún filósofo no es químico).
    Responde solo con: Sí, No
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
        caso="Silogismo avanzado múltiples premisas",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Transformación simbólica",
        caso="Silogismo avanzado múltiples premisas",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_silogismo_avanzado()