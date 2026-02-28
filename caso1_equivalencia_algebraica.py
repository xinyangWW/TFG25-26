import requests
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None

def run_case_1():
    prompt_base = "Resuelve la ecuación: 2(x + 3) = 14"
    prompt_transformado = "Resuelve la ecuación: 2x + 6 = 14"

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 1 ===")


if __name__ == "__main__":
    run_case_1()
