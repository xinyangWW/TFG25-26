import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

MAPA_MODELOS = {
    "chatgpt": "ChatGPT",
    "gemma": "Gemma",
    "deepseek": "DeepSeek"
}

def cargar_datos():
    dataframes = []

    for archivo in BASE_DIR.glob("metricas_resultados_finales_*.csv"):
        modelo_raw = archivo.stem.replace("metricas_resultados_finales_", "")

        modelo = next(
            (MAPA_MODELOS[k] for k in MAPA_MODELOS if k in modelo_raw.lower()),
            modelo_raw
        )

        df = pd.read_csv(archivo)

        df["modelo"] = modelo
        dataframes.append(df)

    return pd.concat(dataframes, ignore_index=True)


def graficas_por_categoria(df: pd.DataFrame):
    categorias = df["tipo_relacion"].unique()

    for categoria in categorias:
        subset = df[df["tipo_relacion"] == categoria]

        orden = ["ChatGPT", "DeepSeek", "Gemma"]
        subset = subset.set_index("modelo").loc[orden].reset_index()

        plt.figure()

        plt.bar(subset["modelo"], subset["porcentaje_acierto"])

        plt.title(f"Rendimiento por modelo — {categoria}")
        plt.ylabel("% de acierto")
        plt.xlabel("Modelo")

        plt.ylim(0, 100)
        plt.tight_layout()

        path = BASE_DIR / f"comparacion_{categoria.replace(' ', '_')}.png"
        plt.savefig(path)

        plt.show()


def main():
    df = cargar_datos()
    graficas_por_categoria(df)


if __name__ == "__main__":
    main()