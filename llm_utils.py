import requests

def query_ollama(prompt: str, model="qwen2.5:3b") -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False}
    )
    return response.json().get("response", "Failed to get response from Ollama.")