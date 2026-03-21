import json
from datetime import datetime
from llm_client import generate_response

def qwen_fixer(raw_text: str, fallback_prompt: str, get_secret_func) -> dict:
    """
    Stryż / Fallback Parser – naprawia zepsuty JSON bez zmiany intencji
    Dla szybkości używamy GPT-4o-mini (bardzo tani, zręczny w JSONach).
    """
    print("🔧 Stryż (Fallback Parser) uruchamia się...")

    szablon = '''
{
  "generation_id": 999,
  "timestamp": "2026-03-21T00:00:00Z",
  "model_architecture": "Odczytaj z kontekstu",
  "role_assigned": "Odczytaj z kontekstu",
  "content": {
    "transport_anchor": "Krótkie streszczenie do Wędrowca",
    "ai_directive": {},
    "claim_types": ["LOGICAL"]
  },
  "peer_review": {
    "previous_entry_id": 0,
    "iws_score": 5.0,
    "critique": "Krytyka",
    "correction_proposed": false
  }
}'''

    prompt = f"Oto uszkodzony tekst wygenerowany przez model:\n\n{raw_text}\n\n=== TWOJE ZADANIE ===\nPrzekształć go na PRAWIDŁOWY JSON posiadający DOKŁADNIE PONIŻSZE KLUCZE:\n{szablon}\n\nZachowaj intencje z oryginalnego tekstu! Zwróć tylko JSON."
    
    try:
        fixed_raw = generate_response(
            prompt=prompt,
            system_prompt=fallback_prompt,
            provider="google",
            model_id="gemini-2.5-flash",
            temperature=0.2,
            get_secret_func=get_secret_func
        )
        
        # Wytnij z powłoki markdown, jeśli model uparł się zawrzeć ```json ... ```
        clean_json = fixed_raw.strip()
        if clean_json.startswith("```json"):
            clean_json = clean_json[7:]
        if clean_json.startswith("```"):
            clean_json = clean_json[3:]
        if clean_json.endswith("```"):
            clean_json = clean_json[:-3]
            
        fixed_dict = json.loads(clean_json.strip())
        
        # Ustawiamy meta info
        fixed_dict.setdefault("meta", {})["error_flag"] = True
        return fixed_dict
        
    except Exception as e:
        print(f"Błąd krytyczny podczas działania Fallback Parser: {e}")
        # Return hardcoded valid minimal dict so the script doesn't crash
        return {
            "generation_id": 999,
            "timestamp": datetime.now().isoformat(),
            "model_architecture": "Qwen-Fixer (Hard-Fallback)",
            "role_assigned": "Stryż",
            "content": {"transport_anchor": "CRITICAL_ERROR: Fallback failed", "ai_directive": {}, "claim_types": ["LOGICAL"]},
            "peer_review": {"previous_entry_id": 0, "iws_score": 5.0, "critique": "Data lost due to hard crash", "correction_proposed": False},
            "meta": {"error_flag": True, "hard_fallback": True}
        }
