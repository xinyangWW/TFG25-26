import sys
from query_model import query_model

MODEL = sys.argv[1] if len(sys.argv) > 1 else "ollama"

def caso_factor_comun_con_excepcion(a_value: int):
    # Base: forma factorizada
    prompt_base = (
        f"Para a = {a_value}, resuelve la ecuación: (a - 3)(x - 2) = (a - 3)(x + 1). "
        "Indica si hay casos especiales según el valor de a."
    )

    # Transformado: forma expandida
    prompt_transformado = (
        f"Para a = {a_value}, resuelve la ecuación: "
        f"(a - 3)x - 2(a - 3) = (a - 3)x + (a - 3). "
        "Indica si hay casos especiales según el valor de a."
    )

    respuesta_base = query_model(prompt_base, model=MODEL)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL)

    print(f"\n===== CASO FACTOR COMÚN (a = {a_value}) =====")
    print("\n--- CASO BASE ---")
    print(respuesta_base)

    print("\n--- CASO TRANSFORMADO ---")
    print(respuesta_transformada)

if __name__ == "__main__":
    caso_factor_comun_con_excepcion(5)   # solución normal
    caso_factor_comun_con_excepcion(3)   # caso especial (0=0)