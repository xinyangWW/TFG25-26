import sys
from query_model import query_model

MODEL = sys.argv[1] if len(sys.argv) > 1 else "ollama"

def caso_diferencia_cuadrados(a_value: int):
    # Base: forma factorizada
    prompt_base = (
        f"Para a = {a_value}, resuelve la ecuación: (x - a)(x + a) = 0. "
        "Indica todas las soluciones posibles."
    )

    # Transformado: forma expandida
    prompt_transformado = (
        f"Para a = {a_value}, resuelve la ecuación: x^2 - a^2 = 0. "
        "Indica todas las soluciones posibles."
    )

    respuesta_base = query_model(prompt_base, model=MODEL)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL)

    print(f"\n===== DIFERENCIA DE CUADRADOS (a = {a_value}) =====")
    print("\n--- CASO BASE ---")
    print(respuesta_base)

    print("\n--- CASO TRANSFORMADO ---")
    print(respuesta_transformada)

if __name__ == "__main__":
    caso_diferencia_cuadrados(4)
    caso_diferencia_cuadrados(0) 
