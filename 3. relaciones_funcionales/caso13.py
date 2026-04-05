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


def caso_13_composicion_desplazamiento():
    """
    MR: h(x) = f(x+1) con f(x) = x^2, luego h(2) = f(3) = 9.
    Evaluamos f(3) directamente y h(2) mediante la definición compuesta.
    Resultado esperado: 9.
    """
    prompt_base = (
        "Sea f(x) = x^2. Calcula f(3). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = x^2 y h(x) = f(x + 1). Calcula h(2). "
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
        caso="Caso 13 Funcional: Composición con desplazamiento — f(3) vs h(2)=f(x+1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 13 Funcional: Composición con desplazamiento — f(3) vs h(2)=f(x+1)",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_13_composicion_desplazamiento()
