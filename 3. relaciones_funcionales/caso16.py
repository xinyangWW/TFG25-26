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


def caso_16_doble_inversa():
    """
    MR: Aplicar la inversa dos veces devuelve la función original: (f^-1)^-1 = f.
    f(x) = 3x - 6  →  f^-1(x) = (x + 6) / 3.
    Evaluamos f(4) directamente y (f^-1)^-1(4) = f(4).
    Resultado esperado: 6.
    """
    prompt_base = (
        "Sea f(x) = 3x - 6. Calcula f(4). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f^-1(x) = (x + 6) / 3. "
        "Sabiendo que la inversa de f^-1 es f(x) = 3x - 6, "
        "calcula f(4) aplicando la inversa de f^-1 en x = 4. "
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
        caso="Caso 16 Funcional: Doble inversa — f(4) vs (f^-1)^-1(4) con f(x)=3x-6",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 16 Funcional: Doble inversa — f(4) vs (f^-1)^-1(4) con f(x)=3x-6",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_16_doble_inversa()
