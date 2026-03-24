import csv
import os
from typing import Any

RESULTS_FILE = "resultados.csv"


def inicializar_resultados() -> None:
    """
    Crea el archivo CSV con cabecera si todavía no existe.
    """
    if not os.path.exists(RESULTS_FILE):
        with open(RESULTS_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "modelo",
                "tipo_relacion",
                "caso",
                "resultado_base",
                "resultado_transformado",
                "cumple_mr",
                "tiempo_segundos",
            ])


def guardar_resultado(
    modelo: str,
    tipo: str,
    caso: str,
    resultado_base: Any,
    resultado_transformado: Any,
    cumple_mr: bool,
    tiempo: float,
) -> None:
    """
    Añade una fila al archivo de resultados.
    """
    inicializar_resultados()

    with open(RESULTS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            modelo,
            tipo,
            caso,
            str(resultado_base),
            str(resultado_transformado),
            cumple_mr,
            round(tiempo, 2),
        ])