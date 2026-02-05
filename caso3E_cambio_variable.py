import requests

def query_model(prompt, model="llama3"):
    """
    Envía un prompt a un modelo de lenguaje ejecutado localmente mediante Ollama
    y devuelve la respuesta generada por el modelo.
    """
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


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
