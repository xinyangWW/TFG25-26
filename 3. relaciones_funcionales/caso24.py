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


def caso_24_horner_vs_estandar():
    """
    MR: La evaluación de un polinomio en forma estándar y en esquema de Horner
    deben dar el mismo resultado.
    f(x) = 2x^3 - 3x^2 + x - 5  →  forma de Horner: ((2x - 3)x + 1)x - 5.
    Evaluamos en x = 4. Resultado esperado: 87.
    """
    prompt_base = (
        "Sea f(x) = 2x^3 - 3x^2 + x - 5. Calcula f(4). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = ((2x - 3) * x + 1) * x - 5. Calcula f(4). "
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
        caso="Caso 24 Funcional: Horner vs estándar — f(4)=2x^3-3x^2+x-5 vs forma de Horner",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 24 Funcional: Horner vs estándar — f(4)=2x^3-3x^2+x-5 vs forma de Horner",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_24_horner_vs_estandar()
