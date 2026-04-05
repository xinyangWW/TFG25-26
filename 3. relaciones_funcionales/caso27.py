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


def caso_27_recurrencia_vs_formula_cerrada():
    """
    MR: Una sucesión definida por recurrencia y su fórmula cerrada equivalente
    deben dar el mismo término.
    Sucesión: a(1) = 3, a(n) = a(n-1) + 4 (progresión aritmética).
    Fórmula cerrada: a(n) = 3 + (n-1) * 4 = 4n - 1.
    Calculamos el término 8. Resultado esperado: 31.
    """
    prompt_base = (
        "Una sucesión cumple: a(1) = 3 y a(n) = a(n-1) + 4 para n > 1. "
        "Calcula a(8). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea a(n) = 4n - 1. Calcula a(8). "
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
        caso="Caso 27 Funcional: Recurrencia vs fórmula cerrada — a(8) con a(n)=a(n-1)+4 vs 4n-1",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 27 Funcional: Recurrencia vs fórmula cerrada — a(8) con a(n)=a(n-1)+4 vs 4n-1",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_27_recurrencia_vs_formula_cerrada()
