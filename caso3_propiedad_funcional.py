import requests
from query_model import query_model

PROVIDER = sys.argv[1] if len(sys.argv) > 1 else "ollama"
MODEL = None

def run_case_3():
    # Definición de la función y evaluación en dos puntos simétricos
    prompt_x = "Sea f(x) = 1+x^2. Calcula f(3)."
    prompt_neg_x = "Sea f(x) = 1+x^2. Calcula f(-3)."

    respuesta_x = query_model(prompt_x)
    respuesta_neg_x = query_model(prompt_neg_x)

    print("=== CASO BASE: f(3) ===")
    print(prompt_x)
    print(respuesta_x)
    print()

    print("=== CASO TRANSFORMADO: f(-3) ===")
    print(prompt_neg_x)
    print(respuesta_neg_x)
    print()

    print("=== FIN DEL CASO 3 ===")


if __name__ == "__main__":
    run_case_3()
