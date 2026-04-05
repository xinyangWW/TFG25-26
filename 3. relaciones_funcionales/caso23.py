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


def caso_23_composicion_inversa_orden_inverso():
    """
    MR: Tanto f(f^-1(x)) como f^-1(f(x)) deben devolver x.
    f(x) = x^3 + 1  →  f^-1(x) = (x - 1)^(1/3).
    f(f^-1(9)) = 9  y  f^-1(f(2)) = 2.
    Probamos ambos órdenes con valores distintos para detectar confusión del modelo.
    Resultado esperado en ambos casos: el valor de entrada (9 y 2 respectivamente).
    """
    prompt_base = (
        "Sea f(x) = x^3 + 1 y su inversa f^-1(x) = (x - 1)^(1/3). "
        "Calcula f(f^-1(9)). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Sea f(x) = x^3 + 1 y su inversa f^-1(x) = (x - 1)^(1/3). "
        "Calcula f^-1(f(2)). "
        "Responde solo con la respuesta, en español."
    )

    start = time.perf_counter()

    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    # Nota: aquí NO comparamos base con transformada entre sí,
    # sino que cada una debe devolver su propio valor de entrada.
    # Usamos evaluar_cumplimiento_mr comparando contra el valor esperado manualmente.
    from mr_utils import normalizar_respuesta
    base_norm  = normalizar_respuesta(respuesta_base)
    transf_norm = normalizar_respuesta(respuesta_transformada)
    cumple_mr   = (base_norm == "9" and transf_norm == "2")
    error_tecnico = base_norm in ("", "ERROR") or transf_norm in ("", "ERROR")

    imprimir_resultados(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 23 Funcional: Composición inversa ambos órdenes — f(f^-1(9))=9 y f^-1(f(2))=2",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 23 Funcional: Composición inversa ambos órdenes — f(f^-1(9))=9 y f^-1(f(2))=2",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_23_composicion_inversa_orden_inverso()
