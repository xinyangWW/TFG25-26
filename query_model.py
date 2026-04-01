import requests
import time
import logging
from typing import Optional

OLLAMA_URL = "http://localhost:11434/api/generate"

AVAILABLE_MODELS = {
    "chatgpt":  "gpt-oss:20b",
    "gemma":    "gemma3:12b",
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
    """Carga el modelo en memoria para que las consultas posteriores sean más rápidas."""
    selected_model = AVAILABLE_MODELS.get(model.lower(), model)
    try:
        SESSION.post(
            OLLAMA_URL,
            json={"model": selected_model, "keep_alive": keep_alive},
            timeout=(5, 30),
        ).raise_for_status()
        logging.info(f"Modelo precargado: {selected_model}")
        print(f"[INFO] Modelo precargado: {selected_model}")
    except Exception as e:
        logging.warning(f"No se pudo precargar {selected_model}: {e}")
        print(f"[WARN] No se pudo precargar {selected_model}: {e}")


def query_model(
    prompt: str,
    model: str = "chatgpt",
    keep_alive: str = "30m",
    think: Optional[bool] = None,
    reintentos: int = 2,
) -> str:
    """
    Envía un prompt al modelo y devuelve la respuesta en texto plano.

    Parámetros:
      - prompt     : texto a enviar al modelo
      - model      : alias del modelo (chatgpt / gemma / deepseek)
      - keep_alive : tiempo que Ollama mantiene el modelo en memoria
      - think      : si True/False, controla el modo razonamiento del modelo
      - reintentos : número de reintentos ante fallos de red (por defecto 2)

    Devuelve:
      - Respuesta del modelo como string
      - "[ERROR ...]" si todos los reintentos fallan (detectable por mr_utils)
    """
    selected_model = AVAILABLE_MODELS.get(model.lower(), model)

    payload = {
        "model":      selected_model,
        "prompt":     prompt,
        "stream":     False,
        "keep_alive": keep_alive,
        "options": {
            "temperature": 0,   # respuestas deterministas
        },
    }
    if think is not None:
        payload["think"] = think

    ultimo_error = None
    for intento in range(1, reintentos + 1):
        try:
            start = time.perf_counter()
            response = SESSION.post(
                OLLAMA_URL,
                json=payload,
                timeout=(5, 180),
            )
            response.raise_for_status()
            data    = response.json()
            elapsed = time.perf_counter() - start
            result  = data.get("response", "").strip()

            # Log resumido: solo los primeros 80 caracteres del prompt
            prompt_resumen = prompt[:80].replace("\n", " ")
            logging.info(
                f"modelo={selected_model} intento={intento} "
                f"tiempo={elapsed:.2f}s prompt={prompt_resumen!r}"
            )
            return result

        except Exception as e:
            ultimo_error = e
            logging.warning(
                f"modelo={selected_model} intento={intento}/{reintentos} error={e}"
            )
            if intento < reintentos:
                time.sleep(2)

    logging.error(f"modelo={selected_model} falló tras {reintentos} intentos: {ultimo_error}")
    return f"[ERROR con modelo {selected_model}] {ultimo_error}"
