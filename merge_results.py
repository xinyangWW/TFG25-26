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

print(f"\n{'=' * 50}  MERGE DE RESULTADOS  {'=' * 50}\n")

for modelo in MODELOS:
    archivos = list(BASE_DIR.glob(f"resultados_{modelo}_*.csv"))

    if not archivos:
        print(f"[AVISO] Sin archivos para '{modelo}'")
        continue

    df = pd.concat((pd.read_csv(f) for f in archivos), ignore_index=True)
    df.to_csv(BASE_DIR / f"resultados_finales_{modelo}.csv", index=False)

    resumen = df.groupby("tipo_relacion")["cumple_mr"].agg(["sum", "count"])
    total, cumple = len(df), df["cumple_mr"].sum()

    print(f"\n── {modelo.upper()} ── {total} casos | Cumple MR: {cumple} ({100 * cumple / total:.1f}%)")
    for tipo, row in resumen.iterrows():
        print(f"   {tipo:<35} {int(row['sum'])}/{int(row['count'])} ({100 * row['sum'] / row['count']:.1f}%)")

print(f"\n{'=' * 50}\n")