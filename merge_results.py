"""
Este archivo genera los siguientes CSVs finales por modelo a partir de resultados_chatgpt_<nombre_persona> de los 3 integrantes del grupo
e imprime un resumen estadístico:
    resultados_finales_chatgpt.csv
    resultados_finales_gemma.csv
    resultados_finales_deepseek.csv
"""
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
MODELOS = ["chatgpt", "gemma", "deepseek"]

CABECERA = [
    "modelo", "tipo_relacion", "caso",
    "resultado_base", "resultado_transformado",
    "cumple_mr", "error_tecnico", "tiempo_segundos",
]


def combinar(modelo: str) -> None:
    archivos = list(BASE_DIR.glob(f"resultados_{modelo}_*.csv"))

    if not archivos:
        print(f"[AVISO] Sin archivos para '{modelo}'")
        return

    # Leer y concatenar
    df = pd.concat((pd.read_csv(f) for f in archivos), ignore_index=True)

    # Asegurar columnas (por si falta alguna)
    df = df.reindex(columns=CABECERA)

    # Guardar CSV final
    salida = BASE_DIR / f"resultados_finales_{modelo}.csv"
    df.to_csv(salida, index=False)

    # Convertir a booleanos
    cumple = df["cumple_mr"].astype(str).str.lower() == "true"
    errores = df["error_tecnico"].astype(str).str.lower() == "true"

    total = len(df)
    total_cumple = cumple.sum()
    total_errores = errores.sum()

    pct = (100 * total_cumple / total) if total else 0

    print(f"\n── {modelo.upper()} ── {total} casos | Cumple MR: {total_cumple} ({pct:.1f}%) | Errores: {total_errores}")

    # Estadísticas por tipo
    resumen = (
        df.assign(cumple_mr_bool=cumple)
        .groupby("tipo_relacion")["cumple_mr_bool"]
        .agg(["count", "sum"])
        .sort_index()
    )

    for tipo, row in resumen.iterrows():
        t = row["count"]
        c = row["sum"]
        print(f"   {tipo:<35} {c}/{t} ({100*c/t:.1f}%)")

    print(f"   → {salida.name}")


if __name__ == "__main__":
    print(f"\n{'='*50}  MERGE DE RESULTADOS  {'='*50}\n")
    for modelo in MODELOS:
        combinar(modelo)
    print(f"\n{'='*50}\n")