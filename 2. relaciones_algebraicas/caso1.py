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

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"

def caso_diferencia_cuadrados(a_value: int):

    prompt_base = (
        f"Para a = {a_value}, resuelve: (x - a)(x + a) = 0. "
        "Responde solo con las soluciones."
    )

    prompt_transformado = (
        f"Para a = {a_value}, resuelve: x^2 - a^2 = 0. "
        "Responde solo con las soluciones."
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

    print("\n===== RESULTADO =====")
    print(f"Modelo: {MODEL}")
    print("Tipo de relación: Algebraica")
    print(f"Caso: Diferencia de cuadrados (a = {a_value})")

    print("\nResultado base:")
    print(respuesta_base)

    print("\nResultado transformado:")
    print(respuesta_transformada)

    print("\nCumple relación metamórfica:")
    print(cumple_mr)

    print("\nTiempo total:")
    print(f"{elapsed:.2f} segundos")

    # AQUÍ se guarda el resultado
    guardar_resultado(
        modelo=MODEL,
        tipo="Algebraica",
        caso=f"Diferencia de cuadrados (a = {a_value})",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":

    preload_model(MODEL)

    caso_diferencia_cuadrados(4)
    caso_diferencia_cuadrados(0)
