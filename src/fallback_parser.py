"""
HEINITZ-PRIME: Fallback Parser (Stryż)
Uses Gemini (not Qwen) for stability on Kaggle during dry-run.
"""
import re
import json
from src.llm_client import generate_response


FALLBACK_PROMPT = """You are a JSON repair specialist. 
The following text contains a broken or incomplete JSON response.
Your task: Extract or reconstruct valid JSON that matches the expected schema.
Return ONLY valid JSON. No markdown. No explanations.

Broken input:"""


def cleanup_markdown_json(text: str) -> str:
    """Remove markdown code blocks and extract JSON"""
    # Remove ```json ... ``` blocks
    text = re.sub(r'```json\s*', '', text)
    text = re.sub(r'```\s*', '', text)
    # Remove leading/trailing whitespace
    text = text.strip()
    return text


def extract_json_from_text(text: str) -> str:
    """Extract first JSON object from text"""
    # Try to find { ... } block
    match = re.search(r'\{.*\}', text, re.DOTALL)
    if match:
        return match.group()
    return text


def qwen_fixer(raw_text: str, fallback_prompt: str, get_secret_func) -> dict:
    """
    Attempt to fix broken JSON using LLM (Gemini for dry-run stability).
    Returns parsed dict or raises exception.
    """
    # Step 1: Clean markdown
    cleaned = cleanup_markdown_json(raw_text)
    
    # Step 2: Try direct parse first
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        pass
    
    # Step 3: Extract JSON block
    json_block = extract_json_from_text(cleaned)
    try:
        return json.loads(json_block)
    except json.JSONDecodeError:
        pass
    
    # Step 4: Call LLM to fix (Gemini, not Qwen — more stable on Kaggle)
    try:
        prompt = f"{fallback_prompt}\n\n{raw_text[:3000]}"  # Truncate for speed
        fixed_raw = generate_response(
            prompt=prompt,
            system_prompt="Return ONLY valid JSON. No markdown. No explanations.",
            provider="google",  # ✅ Gemini instead of huggingface
            model_id="models/gemini-2.5-flash-lite",  # ✅ Fast + stable
            temperature=0.1,
            get_secret_func=get_secret_func
        )
        fixed_cleaned = cleanup_markdown_json(fixed_raw)
        return json.loads(fixed_cleaned)
    except Exception as e:
        print(f"❌ Fallback Parser LLM failed: {e}")
        # Step 5: Hard fallback — return minimal valid structure
        return {
            "content": {
                "text": raw_text[:500],
                "claim_types": ["LOGICAL"]
            },
            "meta": {
                "model": "fallback_hard",
                "generation": 0,
                "peer_review": {
                    "iws_score": 5.0,
                    "reviewer": "fallback_system"
                }
            },
            "errors": [str(e)]
        }


def validate_schema(data: dict, schema: dict) -> tuple[bool, list]:
    """Basic schema validation — check required keys exist"""
    errors = []
    required_top = ["content", "meta"]
    for key in required_top:
        if key not in data:
            errors.append(f"Missing required key: {key}")
    
    if "content" in data:
        if "text" not in data["content"]:
            errors.append("Missing content.text")
    
    if "meta" in data:
        if "model" not in data["meta"]:
            errors.append("Missing meta.model")
        if "generation" not in data["meta"]:
            errors.append("Missing meta.generation")
    
    return (len(errors) == 0, errors)