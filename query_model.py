import os
import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

# OLLAMA (llama3)
def _query_ollama(prompt, model="llama3"):
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

# OPENAI (ChatGPT)
def _query_openai(prompt, model="gpt-4o-mini"):
    from openai import OpenAI

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta OPENAI_API_KEY en variables de entorno.")

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text

# GEMINI (Google)
def _query_gemini(prompt, model="gemini-2.5-flash"):
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta GEMINI_API_KEY en variables de entorno.")

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model=model,
        contents=prompt
    )

    return response.text

# GROK (xAI)
def _query_grok(prompt, model="grok-2-latest"):
    from openai import OpenAI

    api_key = os.environ.get("XAI_API_KEY")
    if not api_key:
        raise RuntimeError("Falta XAI_API_KEY en variables de entorno.")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.x.ai/v1"
    )

    response = client.responses.create(
        model=model,
        input=prompt
    )

    return response.output_text

# FUNCIÓN PRINCIPAL con todas las IAs
def query_model(prompt, provider="ollama", model=None):
    provider = provider.lower()

    if provider == "ollama":
        return _query_ollama(prompt, model or "llama3")

    elif provider == "openai":
        return _query_openai(prompt, model or "gpt-4o-mini")

    elif provider == "gemini":
        return _query_gemini(prompt, model or "gemini-1.5-flash")

    elif provider == "grok":
        return _query_grok(prompt, model or "grok-2-latest")

    else:
        raise ValueError(f"Proveedor no soportado: {provider}")
