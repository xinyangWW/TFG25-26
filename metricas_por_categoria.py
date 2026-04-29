"""
Calcula métricas por tipo_relacion y genera gráfica.
Uso:
    python metricas_por_categoria.py chatgpt
    python metricas_por_categoria.py gemma
    python metricas_por_categoria.py deepseek
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

MODEL    = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"
BASE_DIR = Path(__file__).resolve().parent

CATEGORIA_NUM = {
    "Aritmética":               "1",
    "Algebraica":               "2",
    "Relaciones funcionales":   "3",
    "Transformacion simbolica": "4",
    "Invariancia estructural":  "5",
    "Generalizacion":           "6",
    "Verificacion solucion":    "7",
    "Contexto previo":          "8",
}


def encontrar_csv(modelo: str) -> Path:
    archivos = sorted(BASE_DIR.glob(f"resultados_finales_{modelo}*.csv"))
    if not archivos:
        raise FileNotFoundError(f"No se encontró ningún CSV para '{modelo}'")
    if len(archivos) == 1:
        return archivos[0]
    [print(f"{i}. {a.name}") for i, a in enumerate(archivos, 1)]
    opcion = int(input("\nSelecciona el número del archivo: ")) - 1
    if not (0 <= opcion < len(archivos)):
        raise ValueError("Selección no válida.")
    return archivos[opcion]


def calcular_resumen(df: pd.DataFrame) -> pd.DataFrame:
    df["cumple_mr_bin"] = df["cumple_mr"].apply(
        lambda v: int(str(v).strip().lower() in {"true", "1", "sí", "si"})
    )
    return (
        df.groupby("tipo_relacion")["cumple_mr_bin"]
        .agg(aciertos="sum", total="count")
        .assign(porcentaje_acierto=lambda r: (100 * r["aciertos"] / r["total"]).round(2))
        .reset_index()
    )


def imprimir_resumen(resumen: pd.DataFrame) -> None:
    print(f"\n{'='*30}\nMÉTRICAS POR TIPO_RELACION — {MODEL}\n{'='*30}\n")
    for _, row in resumen.iterrows():
        num = CATEGORIA_NUM.get(row["tipo_relacion"], "?")
        print(f"{num}. {row['tipo_relacion']:<25} {int(row['aciertos'])}/{int(row['total'])} ({row['porcentaje_acierto']:.1f}%)")


def guardar_grafica(resumen: pd.DataFrame, stem: str) -> Path:
    etiquetas = [f"{CATEGORIA_NUM.get(t, '?')}. {t}" for t in resumen["tipo_relacion"]]
    plt.figure()
    plt.bar(etiquetas, resumen["porcentaje_acierto"])
    plt.ylabel("% de acierto")
    plt.xticks(rotation=45)
    plt.tight_layout()
    path = BASE_DIR / f"grafica_{stem}_por_tipo_relacion.png"
    plt.savefig(path)
    plt.show()
    return path


# ── Main ─────────────────────────────────────────────────────────────────────
csv_path = encontrar_csv(MODEL)
df       = pd.read_csv(csv_path)
resumen  = calcular_resumen(df)

imprimir_resumen(resumen)

salida = BASE_DIR / f"metricas_{csv_path.stem}_por_tipo_relacion.csv"
resumen.to_csv(salida, index=False, encoding="utf-8-sig")

grafica = guardar_grafica(resumen, csv_path.stem)
print(f"\nCSV usado:     {csv_path.name}")
print(f"CSV generado:  {salida.name}")
print(f"Gráfica:       {grafica.name}\n")
