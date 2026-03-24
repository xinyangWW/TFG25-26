def evaluar_cumplimiento_mr(respuesta_base: str, respuesta_transformada: str) -> tuple[bool, bool]:
    """
    Devuelve:
    - cumple_mr: True si ambas respuestas no están vacías y son iguales
    - error_tecnico: True si alguna respuesta está vacía
    """

    base_limpia = respuesta_base.strip()
    transformada_limpia = respuesta_transformada.strip()

    error_tecnico = (
        base_limpia == ""
        or transformada_limpia == ""
    )

    cumple_mr = (
        not error_tecnico
        and base_limpia == transformada_limpia
    )

    return cumple_mr, error_tecnico