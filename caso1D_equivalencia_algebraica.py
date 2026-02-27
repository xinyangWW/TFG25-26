import sys
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None

def run_case_1D():
    prompt_base = "Resuelve la ecuación: -2(x - 3) = 4"
    prompt_transformado = "Resuelve la ecuación: -2x + 6 = 4"

    respuesta_base = query_model(prompt_base, provider=PROVIDER, model=MODEL)
    respuesta_transformada = query_model(prompt_transformado, provider=PROVIDER, model=MODEL)

    print("=== CASO BASE (1D) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (1D) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 1D ===")


if __name__ == "__main__":
    run_case_1D()
