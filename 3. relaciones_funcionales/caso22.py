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


def caso_22_funcion_implicita_explicita():
    """
    MR: Una relación implícita y su forma explícita equivalente deben dar
    el mismo valor de y para un x dado.
    Implícita: x^2 + y = 2x + 8. Explícita: y = -(x^2) + 2x + 8.
    Evaluamos en x = 3. Resultado esperado: 5.
    """
    prompt_base = (
        "Dada la ecuación x^2 + y = 2x + 8, despeja y y calcula su valor para x = 3. "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea y = -x^2 + 2x + 8. Calcula y para x = 3. "
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
        caso="Caso 22 Funcional: Implícita vs explícita — x^2+y=2x+8 vs y=-x^2+2x+8 en x=3",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 22 Funcional: Implícita vs explícita — x^2+y=2x+8 vs y=-x^2+2x+8 en x=3",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_22_funcion_implicita_explicita()
