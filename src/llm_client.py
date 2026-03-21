import os
import requests

def call_openai_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "temperature": temperature,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def call_anthropic_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    headers = {
        "x-api-key": api_key, 
        "anthropic-version": "2023-06-01", 
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,
        "temperature": temperature,
        "max_tokens": 4000,
        "system": system_prompt,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["content"][0]["text"]

def call_google_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    # Use Gemini REST API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
    if "gemma" in model_id.lower():
        # Gemma does not support system_instruction in the REST API
        payload = {
            "contents": [{
                "parts": [{"text": f"{system_prompt}\n\nUSER INPUT:\n{prompt}"}]
            }],
            "generationConfig": {
                "temperature": temperature
            }
        }
    else:
        payload = {
            "system_instruction": {
                "parts": [{"text": system_prompt}]
            },
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": temperature
            }
        }
    resp = requests.post(url, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

def call_huggingface_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {
        "model": model_id,
        "temperature": temperature,
        "max_tokens": 4000,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    url = "https://router.huggingface.co/v1/chat/completions"
    resp = requests.post(url, headers=headers, json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

def generate_response(prompt: str, system_prompt: str, provider: str, model_id: str, temperature: float, get_secret_func) -> str:
    """Wrapper to call appropriate API based on provider."""
    try:
        if provider == "openai":
            api_key = get_secret_func("OPENAI_API_KEY")
            return call_openai_model(prompt, system_prompt, model_id, temperature, api_key)
        elif provider == "anthropic":
            api_key = get_secret_func("ANTHROPIC_API_KEY")
            return call_anthropic_model(prompt, system_prompt, model_id, temperature, api_key)
        elif provider == "google":
            api_key = get_secret_func("GOOGLE_API_KEY") or get_secret_func("Gemini API Key")
            return call_google_model(prompt, system_prompt, model_id, temperature, api_key)
        elif provider == "huggingface":
            api_key = get_secret_func("HF_TOKEN") or get_secret_func("Qwen")
            return call_huggingface_model(prompt, system_prompt, model_id, temperature, api_key)
        else:
            raise ValueError(f"Unknown provider: {provider}")
    except Exception as e:
        print(f"Error calling {provider} API: {e}")
        raise
