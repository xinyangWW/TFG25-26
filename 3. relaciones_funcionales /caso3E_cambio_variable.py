import requests
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None

def run_case_3E():
    # Caso base: evaluación directa
    prompt_base = "Sea f(x) = x^2. Calcula f(3)."

    # Caso transformado: cambio de variable equivalente
    prompt_transformado = (
        "Sea f(x) = x^2 y h(x) = f(x + 1). "
        "Calcula h(2)."
    )

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE (3E) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (3E) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 3E ===")


if __name__ == "__main__":
    run_case_3E()
