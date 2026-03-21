"""
HEINITZ-PRIME: LLM Client Wrapper (Dry-Run Minimal)
Providers: huggingface (via OpenAI SDK + router), google (Gemini REST)
Secrets (Kaggle UI): "Qwen", "Gemini API Key", "QDRANT_URL", "QDRANT_API_KEY"
"""
from openai import OpenAI  # ✅ Nowa dependencja
import requests

# ============================================================================
# PROVIDER: HUGGINGFACE (via OpenAI SDK + router.huggingface.co)
# ============================================================================
def call_huggingface_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    """Call HF models via OpenAI-compatible router endpoint"""
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",  # ✅ Bez trailing spaces
        api_key=api_key
    )
    completion = client.chat.completions.create(
        model=model_id,  # ✅ Model w payload, nie w URL
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=4000
    )
    return completion.choices[0].message.content

# ============================================================================
# PROVIDER: GOOGLE (Gemini via REST API) — bez zmian, działa
# ============================================================================
def call_google_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    """Call Gemini via Google Generative Language REST API"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_id}:generateContent?key={api_key}"
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
    resp = requests.post(url, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"]

# ============================================================================
# MAIN WRAPPER: generate_response (DRY-RUN: HF + GEMINI ONLY)
# ============================================================================
def generate_response(prompt: str, system_prompt: str, provider: str, model_id: str, temperature: float, get_secret_func) -> str:
    """
    Wrapper to call appropriate API based on provider.
    Dry-run supports: 'huggingface', 'google'
    """
    try:
        if provider == "huggingface":
            api_key = get_secret_func("Qwen")  # ✅ Exact Kaggle Secret name
            return call_huggingface_model(prompt, system_prompt, model_id, temperature, api_key)
        
        elif provider == "google":
            api_key = get_secret_func("Gemini API Key")  # ✅ Exact Kaggle Secret name
            return call_google_model(prompt, system_prompt, model_id, temperature, api_key)
        
        else:
            raise ValueError(f"Unknown provider for dry-run: {provider}")
    
    except Exception as e:
        print(f"Error calling {provider} API: {e}")
        raise