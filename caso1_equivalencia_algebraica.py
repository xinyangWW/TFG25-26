import requests

def query_model(prompt, model="llama3"):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]


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
