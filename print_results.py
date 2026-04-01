from mr_utils import normalizar_respuesta

# Colores ANSI para la terminal
_VERDE   = "\033[92m"
_ROJO    = "\033[91m"
_RESET   = "\033[0m"
_NEGRITA = "\033[1m"


def imprimir_resultados(
    modelo: str,
    tipo: str,
    caso: str,
    resultado_base: str,
    resultado_transformado: str,
    cumple_mr: bool,
    tiempo: float,
) -> None:
    """
    Imprime por consola el resultado de un caso de prueba metamórfico.
    Muestra también los valores normalizados para facilitar la depuración.
    """
    base_norm   = normalizar_respuesta(resultado_base)
    transf_norm = normalizar_respuesta(resultado_transformado)
    estado      = f"{_VERDE}✔  TRUE{_RESET}" if cumple_mr else f"{_ROJO}✘  FALSE{_RESET}"

    print(f"\n{_NEGRITA}===== RESULTADO ====={_RESET}")
    print(f"Modelo:              {modelo}")
    print(f"Tipo de relación:    {tipo}")
    print(f"Caso:                {caso}")

    print(f"\nResultado base:")
    print(f"  {resultado_base}")
    print(f"  → normalizado: {base_norm}")

    print(f"\nResultado transformado:")
    print(f"  {resultado_transformado}")
    print(f"  → normalizado: {transf_norm}")

    print(f"\nCumple relación metamórfica: {estado}")
    print(f"Tiempo total:        {tiempo:.2f} segundos")
