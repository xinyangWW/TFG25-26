import sys
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None

def run_case_5():
    # Misma ecuación, distinta variable (renombrado simbólico)
    prompt_base = "Resuelve para x: x^2 - 9 = 0"
    prompt_transformado = "Resuelve para y: y^2 - 9 = 0"

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE (5) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (5) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 5 ===")

if __name__ == "__main__":
    run_case_5()
