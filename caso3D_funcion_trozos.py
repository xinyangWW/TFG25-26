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


def run_case_3D():
    # Caso base: definición estándar
    prompt_base = (
        "Sea f(x) definida como: "
        "f(x) = x^2 si x ≥ 0 y f(x) = −x si x < 0. "
        "Calcula f(-2)."
    )

    # Caso transformado: misma definición, distinto orden
    prompt_transformado = (
        "Sea f(x) definida a trozos: "
        "si x < 0 entonces f(x) = −x, "
        "si x ≥ 0 entonces f(x) = x^2. "
        "Calcula f(-2)."
    )

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE (3D) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (3D) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 3D ===")


if __name__ == "__main__":
    run_case_3D()
