import os
from typing import Any

try:
    import ollama
except Exception:  # pragma: no cover
    ollama = None


def get_ollama_config():
    return {
        'host': os.getenv('OLLAMA_HOST', 'http://localhost:11434'),
        'model': os.getenv('OLLAMA_MODEL', 'qwen2.5-coder:3b'),
    }


def chat_with_ollama(messages, model=None, host=None):
    if ollama is None:
        return None, 'Ollama Python library is unavailable.'

    model_name = model or get_ollama_config()['model']
    host_value = host or get_ollama_config()['host']

    try:
        ollama.Client(host=host_value)
    except Exception as exc:  # pragma: no cover
        return None, f'Ollama server is unavailable: {exc}'

    try:
        response = ollama.chat(
            model=model_name,
            messages=messages,
            stream=False,
            options={'temperature': 0.2},
        )
        content = response.get('message', {}).get('content') if isinstance(response, dict) else None
        if not content:
            return None, 'Ollama returned an empty response.'
        return content, None
    except Exception as exc:  # pragma: no cover
        return None, f'Ollama request failed: {exc}'
