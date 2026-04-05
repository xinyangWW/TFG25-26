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
TIPO = "Relaciones funcionales"


def caso_30_racional_descomposicion_parcial():
    """
    MR: Una función racional y su descomposición en fracciones parciales
    deben dar el mismo resultado al evaluarlas.
    f(x) = (2x + 1) / ((x)(x + 1)).
    Descomposición: f(x) = 1/x + 1/(x+1).
    Evaluamos en x = 4. Resultado esperado: 9/20 = 0.45.
    """
    prompt_base = (
        "Sea f(x) = (2x + 1) / (x * (x + 1)). Calcula f(4) como número decimal. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = 1/x + 1/(x + 1). Calcula f(4) como número decimal. "
        "Responde solo con la respuesta, en español."
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
        caso="Caso 30 Funcional: Fracciones parciales — f(4)=(2x+1)/(x(x+1)) vs 1/x+1/(x+1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 30 Funcional: Fracciones parciales — f(4)=(2x+1)/(x(x+1)) vs 1/x+1/(x+1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_30_racional_descomposicion_parcial()
