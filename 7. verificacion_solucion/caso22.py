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
from mr_utils import evaluar_cumplimiento_mr, evaluar_solucion_general, extraer_soluciones, formatear_soluciones
from print_results import imprimir_resultados

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_22_sistema_4_incognitas():

    # Caso base:
    sistema = ["x + 2*y - z + 3*t = -8", "2*x + 2*z -t = 13", 
               "-x + y + z - t = 8", "3*x +3*y - z + 2*t = -1"]
    sistema_str = ", ".join(sistema)

    prompt_base = (
        f"Calcula las soluciones del siguiente sistema de ecuaciones: {sistema_str}. "
        "Responde SOLO con números, sin texto adicional."
    )

    start = time.perf_counter()

    respuesta_base = query_model(
        prompt_base,
        model=MODEL,
        think=False
    )

    satisfy, error = evaluar_solucion_general(respuesta_base, sistema, variables=('x', 'y', 'z', 't'))

    valores = extraer_soluciones(respuesta_base, ('x', 'y', 'z', 't'))
    valores_str = formatear_soluciones(valores)

    prompt_transformado = (
        f"Comprueba si {valores_str} satisface el sistema de ecuaciones {sistema_str}. "
        "Responde SI o NO, sin texto adicional."
    )

    respuesta_transformada = query_model(
        prompt_transformado,
        model=MODEL,
        think=False
    )

    elapsed = time.perf_counter() - start

    modelo_verifica = "si" in respuesta_transformada.lower()
    cumple_mr = (satisfy == modelo_verifica)
    error_tecnico = error

    imprimir_resultados(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la solución al sistema de ecuaciones {sistema}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo="Verificación de solución",
        caso=f"Evaluación de la solución al sistema de ecuaciones {sistema_str}",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )

if __name__ == "__main__":

    preload_model(MODEL)

    caso_22_sistema_4_incognitas()