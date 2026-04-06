"""
Ejecuta todos los casos de las carpetas del proyecto para el modelo indicado.

Uso:
    python run_all.py chatgpt
    python run_all.py gemma
    python run_all.py deepseek

Resultado: resultados_chatgpt.csv / resultados_gemma.csv / resultados_deepseek.csv
"""

import sys, runpy, traceback
import pandas as pd
from pathlib import Path
from query_model import preload_model

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"
BASE_DIR = Path(__file__).resolve().parent
CARPETAS = sorted(p for p in BASE_DIR.iterdir() if p.is_dir() and p.name[0].isdigit())

print(f"\n{'='*50}\nModelo: {MODEL.upper()} — {len(CARPETAS)} categorías\n{'='*50}")
preload_model(MODEL)

total = errores = 0

for carpeta in CARPETAS:
    archivos = sorted(carpeta.glob("caso*.py"))
    print(f"\n── {carpeta.name} ({len(archivos)} casos) ──")
    for archivo in archivos:
        print(f"  ▶ {archivo.name}")
        try:
            sys.argv = [str(archivo), MODEL]
            runpy.run_path(str(archivo), run_name="__main__")
            total += 1
        except Exception as e:
            print(f"  [ERROR] {archivo.name}: {e}")
            traceback.print_exc()
            errores += 1

# Resumen con pandas
df = pd.read_csv(BASE_DIR / f"resultados_{MODEL}.csv")
resumen = df.groupby("tipo_relacion")["cumple_mr"].agg(["sum", "count"])

print(f"\n{'='*60}\nCompletado: {total} casos, {errores} errores\n")
for tipo, row in resumen.iterrows():
    print(f"  {tipo:<35} {int(row['sum'])}/{int(row['count'])} ({100*row['sum']/row['count']:.1f}%)")
print(f"\nCSV: resultados_{MODEL}.csv\n{'='*60}\n")
