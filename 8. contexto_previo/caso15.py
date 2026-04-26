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

def caso_15_probabilidad_bayes():

    # Caso base:
    problema = (
        "Una enfermedad afecta al 0.5% de la población. "
        "Un test tiene 98% de sensibilidad y 97% de especificidad. "
        "Una persona obtiene dos resultados positivos consecutivos. "
        "¿Cuál es la probabilidad de que esté enferma?"
    )
    contexto = "ten en cuenta tanto la probabilidad de tener la enfermedad como los falsos positivos del test"
    prompt_base = (
        f"{problema}."
        "Responde SOLO con un número decimal entre 0 y 1, sin texto adicional."
    )

    # Caso transformado:
    prompt_transformado = (
        f"{problema}, {contexto}."
        "Responde SOLO con un número decimal entre 0 y 1, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    cumple_mr, error_tecnico = evaluar_cumplimiento_mr(
        respuesta_base,
        respuesta_transformada
    )

    imprimir_resultados(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Probabilidad tipo Bayes, sin y con contexto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Probabilidad tipo Bayes, sin y con contexto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_15_probabilidad_bayes()