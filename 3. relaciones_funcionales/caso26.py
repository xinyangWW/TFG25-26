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


def caso_26_identidad_pitagorica():
    """
    MR: Identidad pitagórica: sen^2(x) + cos^2(x) = 1 para cualquier x.
    Evaluamos sen^2(30°) + cos^2(30°) directamente
    y comparamos con el valor constante 1.
    Resultado esperado: 1.
    """
    prompt_base = (
        "Calcula sen(30°)^2 + cos(30°)^2, donde el ángulo está en grados. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Usando la identidad trigonométrica fundamental, ¿cuánto vale "
        "sen^2(x) + cos^2(x) para cualquier valor de x? "
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
        caso="Caso 26 Funcional: Identidad pitagórica — sen^2(30)+cos^2(30) vs valor constante",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 26 Funcional: Identidad pitagórica — sen^2(30)+cos^2(30) vs valor constante",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_26_identidad_pitagorica()
