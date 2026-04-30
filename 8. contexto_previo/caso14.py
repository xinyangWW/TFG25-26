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

def caso_14_probabilidad_bayes():

    # Caso base:
    problema = (
        f"Una enfermedad afecta al 1% de la población. "
        f"Un test tiene un 99% de sensibilidad (detecta correctamente a los enfermos) "
        f"y un 95% de especificidad (detecta correctamente a los sanos). "
        "Si una persona da positivo, ¿cuál es la probabilidad de que realmente esté enferma?"
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
        caso=f"Probabilidad tipo Bayes; sin y con contexto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Contexto Previo",
        caso=f"Probabilidad tipo Bayes; sin y con contexto",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_14_probabilidad_bayes()