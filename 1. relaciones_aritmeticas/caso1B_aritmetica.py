import sys
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None  

def caso_parametro_con_excepcion(a_value: int):
    # Base: forma factorizada (factor anulable)
    prompt_base = (
        f"Para a = {a_value}, resuelve la ecuación: (a - 2)(x + 3) = 2(a - 2). "
        "Indica si hay casos especiales según el valor de a."
    )

    # Transformado: forma expandida equivalente
    prompt_transformado = (
        f"Para a = {a_value}, resuelve la ecuación: (a - 2)x + 3(a - 2) = 2(a - 2). "
        "Indica si hay casos especiales según el valor de a."
    )

    respuesta_base = query_model(prompt_base, provider=PROVIDER, model=MODEL)
    respuesta_transformada = query_model(prompt_transformado, provider=PROVIDER, model=MODEL)

    print(f"\n===== CASO PARAMÉTRICO (a = {a_value}) =====")
    print("\n--- CASO BASE ---")
    print(prompt_base)
    print(respuesta_base)

    print("\n--- CASO TRANSFORMADO ---")
    print(prompt_transformado)
    print(respuesta_transformada)

    print("\n===============================\n")

if __name__ == "__main__":

    caso_parametro_con_excepcion(5)

    caso_parametro_con_excepcion(2)
