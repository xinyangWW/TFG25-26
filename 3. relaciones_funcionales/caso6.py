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


def caso_6_funcion_inversa():
    """
    MR: Aplicar una función y su inversa devuelve el valor original.
    f(x) = 2x + 4  →  f^-1(y) = (y - 4) / 2.
    f^-1(f(3)) debe ser igual a 3.
    Formulación base: calcular f(3) y luego aplicar la inversa.
    Formulación transformada: enunciado directo de f^-1(f(3)).
    Resultado esperado: 3.
    """
    prompt_base = (
        "Sea f(x) = 2x + 4. Primero calcula f(3). "
        "Luego, sabiendo que la función inversa es f^-1(y) = (y - 4) / 2, "
        "aplica f^-1 al resultado anterior. "
        "Responde solo con el número final, en español."
    )
    prompt_transformado = (
        "Sea f(x) = 2x + 4 y su función inversa f^-1(y) = (y - 4) / 2. "
        "Calcula f^-1(f(3)). "
        "Responde solo con el número, en español."
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
        caso="Caso 6 Funcional: Función inversa — f^-1(f(3)) en dos formulaciones",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 6 Funcional: Función inversa — f^-1(f(3)) en dos formulaciones",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_6_funcion_inversa()
