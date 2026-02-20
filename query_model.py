import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

def query_model(prompt, model="llama3"):
    response = requests.post(
        OLLAMA_URL,
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json().get("response", "")