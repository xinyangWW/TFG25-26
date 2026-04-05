"""
results_manager.py
------------------
Genera un CSV separado por modelo en la raíz del proyecto:
    resultados_chatgpt.csv
    resultados_gemma.csv
    resultados_deepseek.csv

Cada persona ejecuta sus casos y obtiene sus propios CSVs.
Al final se pueden combinar con merge_results.py.
"""

import csv
import os
from typing import Any
from mr_utils import normalizar_respuesta

_CABECERA = [
    "modelo",
    "tipo_relacion",
    "caso",
    "resultado_base",
    "resultado_transformado",
    "cumple_mr",
    "error_tecnico",
    "tiempo_segundos",
]


def _ruta_csv(modelo: str) -> str:
    """Devuelve la ruta absoluta del CSV para el modelo dado."""
    directorio = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(directorio, f"resultados_{modelo.lower()}.csv")


def inicializar_resultados(modelo: str) -> None:
    """Crea el archivo CSV con cabecera si todavía no existe."""
    ruta = _ruta_csv(modelo)
    if not os.path.exists(ruta):
        with open(ruta, mode="w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(_CABECERA)


def guardar_resultado(
    modelo: str,
    tipo: str,
    caso: str,
    resultado_base: Any,
    resultado_transformado: Any,
    cumple_mr: bool,
    error_tecnico: bool,
    tiempo: float,
) -> None:
    """Añade una fila al CSV del modelo con los valores normalizados."""
    inicializar_resultados(modelo)

    ruta = _ruta_csv(modelo)
    with open(ruta, mode="a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([
            modelo,
            tipo,
            caso,
            normalizar_respuesta(str(resultado_base)),
            normalizar_respuesta(str(resultado_transformado)),
            cumple_mr,
            error_tecnico,
            round(tiempo, 2),
        ])