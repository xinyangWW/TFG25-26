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


def run_case_2():
    prompt_particular = "Calcula la suma de los primeros 100 números naturales." #Es una instancia concreta del problema, con valores específicos.
    prompt_general = (
        "Explica la fórmula para calcular la suma de los primeros n números naturales "#Es la formulación abstracta del mismo problema, usando una variable.
        "y aplícala para n = 100."
    )

    respuesta_particular = query_model(prompt_particular)
    respuesta_general = query_model(prompt_general)

    print("=== CASO PARTICULAR ===")
    print(prompt_particular)
    print(respuesta_particular)
    print()

    print("=== CASO GENERAL ===")
    print(prompt_general)
    print(respuesta_general)
    print()

    print("=== FIN DEL CASO 2 ===")


if __name__ == "__main__":
    run_case_2()
