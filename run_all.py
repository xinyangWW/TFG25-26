"""
Ejecuta todos los casos de las carpetas del proyecto para el modelo indicado.

Uso:
    python run_all.py chatgpt
    python run_all.py gemma
    python run_all.py deepseek

Resultado: resultados_chatgpt.csv / resultados_gemma.csv / resultados_deepseek.csv
"""

import sys
import importlib.util
import inspect
import traceback
from pathlib import Path

from query_model import preload_model

MODEL = sys.argv[1] if len(sys.argv) > 1 else "chatgpt"
BASE_DIR = Path(__file__).resolve().parent

# Carpetas que empiezan por número
CARPETAS = sorted(p for p in BASE_DIR.iterdir() if p.is_dir() and p.name[0].isdigit())

print("\n" + "="*50)
print(f"Modelo: {MODEL.upper()} — {len(CARPETAS)} categorías")
print("="*50)

preload_model(MODEL)

def ejecutar_archivo(ruta: Path) -> None:
    sys.argv = [str(ruta), MODEL]

    # Cargar módulo dinámicamente
    spec = importlib.util.spec_from_file_location("_caso", ruta)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)

    # Ejecutar funciones caso_*
    for nombre in dir(modulo):
        fn = getattr(modulo, nombre)
        if nombre.startswith("caso_") and callable(fn) and not inspect.signature(fn).parameters:
            fn()

total = errores = 0

for carpeta in CARPETAS:
    archivos = sorted(carpeta.glob("caso*.py"))
    print(f"\n── {carpeta.name} ({len(archivos)} casos) ──")

    for archivo in archivos:
        print(f"  ▶ {archivo.name}")
        try:
            ejecutar_archivo(archivo)
            total += 1
        except Exception as e:
            print(f"  [ERROR] {archivo.name}: {e}")
            traceback.print_exc()
            errores += 1

print("\n" + "="*60)
print(f"Completado: {total} casos, {errores} errores")
print(f"CSV: resultados_{MODEL}.csv")
print("="*60 + "\n")