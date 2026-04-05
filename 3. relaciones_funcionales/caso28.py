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


def caso_28_exponencial_logaritmo_inversas():
    """
    MR: La exponencial y el logaritmo son funciones inversas: e^(ln(x)) = x.
    Evaluamos e^(ln(7)) directamente y el valor esperado 7.
    También probamos ln(e^3) = 3.
    Resultado esperado base: 7. Resultado esperado transformado: 3.
    Ambos deben ser coherentes con la propiedad de función inversa.
    """
    prompt_base = (
        "Calcula e elevado a ln(7), es decir, e^(ln(7)). "
        "Responde solo con la respuesta, en español."
    )
    prompt_transformado = (
        "Calcula el logaritmo natural de e^3, es decir, ln(e^3). "
        "Responde solo con la respuesta, en español."
    )

    start = time.perf_counter()

    from mr_utils import normalizar_respuesta
    respuesta_base = query_model(prompt_base, model=MODEL, think=False)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL, think=False)

    elapsed = time.perf_counter() - start

    base_norm   = normalizar_respuesta(respuesta_base)
    transf_norm = normalizar_respuesta(respuesta_transformada)
    cumple_mr   = (base_norm == "7" and transf_norm == "3")
    error_tecnico = base_norm in ("", "ERROR") or transf_norm in ("", "ERROR")

    imprimir_resultados(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 28 Funcional: Exponencial y logaritmo inversas — e^ln(7)=7 y ln(e^3)=3",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        tiempo=elapsed
    )

    guardar_resultado(
        modelo=MODEL,
        tipo=TIPO,
        caso="Caso 28 Funcional: Exponencial y logaritmo inversas — e^ln(7)=7 y ln(e^3)=3",
        resultado_base=respuesta_base,
        resultado_transformado=respuesta_transformada,
        cumple_mr=cumple_mr,
        error_tecnico=error_tecnico,
        tiempo=elapsed
    )


if __name__ == "__main__":
    preload_model(MODEL)
    caso_28_exponencial_logaritmo_inversas()
