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


def caso_29_composicion_no_conmutativa():
    """
    MR: La composición de funciones NO es conmutativa en general.
    f(x) = x + 2, g(x) = x^2.
    f(g(3)) = f(9) = 11.
    g(f(3)) = g(5) = 25.
    El modelo debe dar resultados distintos y coherentes con cada composición.
    Usamos evaluación individual contra valor esperado.
    """
    prompt_base = (
        "Sea f(x) = x + 2 y g(x) = x^2. Calcula f(g(3)). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = x + 2 y g(x) = x^2. Calcula g(f(3)). "
        "Responde solo con la respuesta, en español."
    )

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    from mr_utils import normalizar_respuesta
    base_norm   = normalizar_respuesta(respuesta_base)
    transf_norm = normalizar_respuesta(respuesta_transformada)
    # Ambas respuestas deben ser correctas pero distintas entre sí
    cumple_mr   = (base_norm == "11" and transf_norm == "25")
    error_tecnico = base_norm in ("", "ERROR") or transf_norm in ("", "ERROR")

    imprimir_resultados(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 29 Funcional: Composición no conmutativa — f(g(3))=11 y g(f(3))=25",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 29 Funcional: Composición no conmutativa — f(g(3))=11 y g(f(3))=25",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_29_composicion_no_conmutativa()
