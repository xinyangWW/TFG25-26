import requests
import time
import logging
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"

AVAILABLE_MODELS = {
    "chatgpt": "gpt-oss:20b",
    "gemma": "gemma3:27b",
    "deepseek": "deepseek-r1:8b",
}

# Una sola sesión HTTP para reutilizar conexiones
SESSION = requests.Session()

logging.basicConfig(
    filename="execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def preload_model(model: str = "chatgpt", keep_alive: str = "30m") -> None:
    selected_model = AVAILABLE_MODELS.get(model.lower(), model)
    try:
        SESSION.post(
            OLLAMA_URL,
            json={
                "model": selected_model,
                "keep_alive": keep_alive,
            },
            timeout=(5, 30),
        ).raise_for_status()
        logging.info(f"Modelo precargado: {selected_model}")
    except Exception as e:
        logging.warning(f"No se pudo precargar {selected_model}: {e}")

def query_model(
    prompt: str,
    model: str = "chatgpt",
    keep_alive: str = "30m",
    think: Optional[bool] = None,
) -> str:
    selected_model = AVAILABLE_MODELS.get(model.lower(), model)

    payload = {
        "model": selected_model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": keep_alive,
        # Útil para respuestas cortas y consistentes
        "options": {
            "temperature": 0,
            "num_predict": 20,
        },
    }

    # Solo añade think si lo quieres controlar explícitamente
    if think is not None:
        payload["think"] = think

    start = time.perf_counter()

    try:
        response = SESSION.post(
            OLLAMA_URL,
            json=payload,
            timeout=(5, 180),  # 5s conectar, 180s leer
        )
        response.raise_for_status()
        data = response.json()

        elapsed = time.perf_counter() - start
        result = data.get("response", "").strip()

        logging.info(
            f"modelo={selected_model} tiempo={elapsed:.2f}s prompt={prompt!r}"
        )

        return result

    except Exception as e:
        logging.error(f"Error con {selected_model}: {e}")
        return f"[ERROR con modelo {selected_model}] {e}"

def unload_model(model: str = "chatgpt") -> None:
    selected_model = AVAILABLE_MODELS.get(model.lower(), model)
    try:
        SESSION.post(
            OLLAMA_URL,
            json={
                "model": selected_model,
                "keep_alive": 0,
            },
            timeout=(5, 30),
        ).raise_for_status()
        logging.info(f"Modelo descargado: {selected_model}")
    except Exception as e:
        logging.warning(f"No se pudo descargar {selected_model}: {e}")
