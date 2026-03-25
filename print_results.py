# Función para imprimir los resultados de la ejecución de cada caso
def imprimir_resultados(
    modelo: str,
    tipo: str,
    caso: str,
    resultado_base: str,
    resultado_transformado: str,
    cumple_mr,
    tiempo: float
):
    print("\n===== RESULTADO =====")

    print(f"Modelo: {modelo}")
    print(f"Tipo de relación: {tipo}")
    print(f"Caso: {caso}")

    print("\nResultado base:")
    print(resultado_base)

    print("\nResultado transformado:")
    print(resultado_transformado)

    print("\nCumple relación metamórfica:")
    print(cumple_mr)

    print("\nTiempo total:")
    print(f"{tiempo:.2f} segundos")