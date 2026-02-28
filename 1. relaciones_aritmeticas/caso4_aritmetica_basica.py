from query_model import query_model

def run_case_4():
    # Misma operación, distinta formulación (conmutatividad/asociatividad)
    prompt_base = "Calcula: (7 + 5) * 2"
    prompt_transformado = "Calcula: 2 * (5 + 7)"

    respuesta_base = query_model(prompt_base)
    respuesta_transformada = query_model(prompt_transformado)

    print("=== CASO BASE (4) ===")
    print(prompt_base)
    print(respuesta_base)
    print()

    print("=== CASO TRANSFORMADO (4) ===")
    print(prompt_transformado)
    print(respuesta_transformada)
    print()

    print("=== FIN DEL CASO 4 ===")

if __name__ == "__main__":
    run_case_4()
