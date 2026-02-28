import sys
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None
def run_case_6():

    prompt_base = "Calcula: 12 - 4 * 2"
    prompt_transformado = "Calcula: ((12 - 4 * 2) + 0) * 1"

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE (6) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (6) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 6 ===")

if __name__ == "__main__":
    run_case_6()
