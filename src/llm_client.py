"""
HEINITZ-PRIME: LLM Client Wrapper (Dry-Run Minimal)
Providers: huggingface (Qwen), google (Gemini)
Secrets (Kaggle UI): "Qwen", "Gemini API Key", "QDRANT_API_KEY", "QDRANT_URL"
"""
import requests
import os

# ============================================================================
# PROVIDER: HUGGINGFACE (Qwen via new router endpoint)
# ============================================================================
def call_huggingface_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    """Call HF Inference API v1 via router.huggingface.co — NO TRAILING SPACES"""
    url = "https://router.huggingface.co/hf-inference/v1/chat/completions"  # ✅ No trailing space
    headers = {
        "Authorization": f"Bearer {api_key}",  # ✅ No trailing space after key or value
        "Content-Type": "application/json"
    }
    payload = {
        "model": model_id,  # ✅ model in payload, not URL
        "temperature": temperature,
        "max_tokens": 4000,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }
    resp = requests.post(url, headers=headers, json=payload, timeout=30)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

# ============================================================================
# PROVIDER: GOOGLE (Gemini via REST API)
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
# MAIN WRAPPER: generate_response
# ============================================================================
def generate_response(prompt: str, system_prompt: str, provider: str, model_id: str, temperature: float, get_secret_func) -> str:
    """
    Wrapper to call appropriate API based on provider.
    Dry-run supports: 'huggingface', 'google'
    """
    try:
        if provider == "huggingface":
            api_key = get_secret_func("Qwen")  # ✅ Exact name from Kaggle Secrets UI
            return call_huggingface_model(prompt, system_prompt, model_id, temperature, api_key)
        
        elif provider == "google":
            api_key = get_secret_func("Gemini API Key")  # ✅ Exact name from Kaggle Secrets UI
            return call_google_model(prompt, system_prompt, model_id, temperature, api_key)
        
        # --------------------------------------------------------------------
        # PHASE 2: Uncomment below when adding OpenAI/Anthropic support
        # --------------------------------------------------------------------
        # elif provider == "openai":
        #     api_key = get_secret_func("OPENAI_API_KEY")
        #     return call_openai_model(prompt, system_prompt, model_id, temperature, api_key)
        # elif provider == "anthropic":
        #     api_key = get_secret_func("ANTHROPIC_API_KEY")
        #     return call_anthropic_model(prompt, system_prompt, model_id, temperature, api_key)
        
        else:
            raise ValueError(f"Unknown provider for dry-run: {provider}")
    
    except Exception as e:
        print(f"Error calling {provider} API: {e}")
        raise

# ============================================================================
# PHASE 2: Stubs for future providers (commented out for dry-run minimalism)
# ============================================================================
# def call_openai_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
#     ...
# def call_anthropic_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
#     ...