import sys
from query_model import query_model

MODEL = sys.argv[1] if len(sys.argv) > 1 else "ollama"

def caso_distribucion_con_excepcion(a_value: int):
    # Base: forma compacta
    prompt_base = (
        f"Para a = {a_value}, resuelve la ecuación: a(x + 2) = ax + 4. "
        "Indica si hay casos especiales."
    )

    # Transformado: forma expandida
    prompt_transformado = (
        f"Para a = {a_value}, resuelve la ecuación: ax + 2a = ax + 4. "
        "Indica si hay casos especiales."
    )

    respuesta_base = query_model(prompt_base, model=MODEL)
    respuesta_transformada = query_model(prompt_transformado, model=MODEL)

    print(f"\n===== DISTRIBUCIÓN (a = {a_value}) =====")
    print("\n--- CASO BASE ---")
    print(respuesta_base)

    print("\n--- CASO TRANSFORMADO ---")
    print(respuesta_transformada)

if __name__ == "__main__":
    caso_distribucion_con_excepcion(2)   # solución normal
    caso_distribucion_con_excepcion(0)   # caso especial (0x = 4)