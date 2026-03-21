"""
HEINITZ-PRIME: LLM Client Wrapper (Dry-Run Minimal)
Providers: huggingface (via OpenAI SDK), google (via google.genai SDK)
Secrets (Kaggle UI): "Qwen", "Gemini API Key", "QDRANT_URL", "QDRANT_API_KEY"
"""
from openai import OpenAI
from google import genai


def call_huggingface_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    """Call HF models via OpenAI-compatible router endpoint"""
    client = OpenAI(
        base_url="https://router.huggingface.co/v1",
        api_key=api_key
    )
    completion = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=4000
    )
    return completion.choices[0].message.content


def call_google_model(prompt: str, system_prompt: str, model_id: str, temperature: float, api_key: str) -> str:
    """Call Gemini via google.genai SDK — config dict mode"""
    client = genai.Client(api_key=api_key)
    
    # Normalize model prefix (ensure exactly one "models/")
    if model_id.startswith("models/models/"):
        clean_model = model_model.replace("models/models/", "models/", 1)
    elif model_id.startswith("models/"):
        clean_model = model_id
    else:
        clean_model = f"models/{model_id}"
    
    response = client.models.generate_content(
        model=clean_model,
        contents=f"SYSTEM: {system_prompt}\n\nUSER: {prompt}",
        config={"temperature": temperature, "max_output_tokens": 4000}
    )
    return response.text


def generate_response(prompt: str, system_prompt: str, provider: str, model_id: str, temperature: float, get_secret_func) -> str:
    """
    Wrapper to call appropriate API based on provider.
    Dry-run supports: 'huggingface', 'google'
    """
    try:
        if provider == "huggingface":
            api_key = get_secret_func("Qwen")
            return call_huggingface_model(prompt, system_prompt, model_id, temperature, api_key)
        
        elif provider == "google":
            api_key = get_secret_func("Gemini API Key")
            return call_google_model(prompt, system_prompt, model_id, temperature, api_key)
        
        else:
            raise ValueError(f"Unknown provider for dry-run: {provider}")
    
    except Exception as e:
        print(f"Error calling {provider} API: {e}")
        raise