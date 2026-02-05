import requests

def query_model(prompt, model="llama3"):
    """
    Envía un prompt a un modelo de lenguaje ejecutado localmente mediante Ollama
    y devuelve la respuesta generada.
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


def run_case_2(n):
    """
    Ejecuta el caso de generalización para un valor dado de n,
    comparando el caso particular con la formulación general.
    """
    prompt_particular = f"Calcula la suma de los primeros {n} números naturales."#Es una instancia concreta del problema, con valores específicos.
    prompt_general = (
        "Explica la fórmula para calcular la suma de los primeros n números naturales "#Es la formulación abstracta del mismo problema, usando una variable.
        f"y aplícala para n = {n}."
    )

    respuesta_particular = query_model(prompt_particular)
    respuesta_general = query_model(prompt_general)

    print(f"===== RESULTADOS PARA n = {n} =====")
    print("CASO PARTICULAR:")
    print(respuesta_particular)
    print()
    print("CASO GENERAL:")
    print(respuesta_general)
    print("\n" + "=" * 45 + "\n")


if __name__ == "__main__":
    # Valor pequeño: comportamiento esperado coherente
    run_case_2(100)

    # Valor grande: mayor probabilidad de inconsistencia
    run_case_2(10000)
