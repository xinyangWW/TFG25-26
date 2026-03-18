import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

AVAILABLE_MODELS = {
    "chatgpt": "gpt-oss:20b",
    "gemma": "gemma3:27b",
    "deepseek": "deepseek-r1:8b",
}

def query_model(prompt: str, model: str = "chatgpt") -> str:
    """
    Envía un prompt a un modelo ejecutado localmente mediante Ollama
    y devuelve la respuesta generada.

    Modelos disponibles:
    - chatgpt -> gpt-oss:20b
    - gemma  -> gemma3:27b
    - deepseek    -> deepseek-r1:8b
    """

    selected_model = AVAILABLE_MODELS.get(model.lower(), model)

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": selected_model,
                "prompt": prompt,
                "stream": False,
            },
            timeout=120,
        )

        response.raise_for_status()
        data = response.json()

        return data.get("response", "").strip()

    except Exception as e:
        return f"[ERROR con modelo {selected_model}] {str(e)}"
