from query_model import query_model

def run_case_7():
    # Verificación: la solución propuesta debe satisfacer la ecuación.
    # Usamos una ecuación con solución conocida para no depender de parseo automático.
    ecuacion = "2x + 3 = 11"
    solucion_correcta = "4"

    prompt_resolver = f"Resuelve la ecuación: {ecuacion}"
    prompt_verificar = f"Comprueba si x = {solucion_correcta} es solución de la ecuación: {ecuacion}. Justifica sustituyendo."

    respuesta_resolver = query_model(prompt_resolver)
    respuesta_verificar = query_model(prompt_verificar)

    print("=== CASO BASE (7): RESOLVER ===")
    print(prompt_resolver)
    print(respuesta_resolver)
    print()

    print("=== CASO TRANSFORMADO (7): VERIFICAR ===")
    print(prompt_verificar)
    print(respuesta_verificar)
    print()

    print("=== FIN DEL CASO 7 ===")

if __name__ == "__main__":
    run_case_7()
