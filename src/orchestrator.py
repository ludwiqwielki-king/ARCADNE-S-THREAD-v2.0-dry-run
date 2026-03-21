#!/usr/bin/env python3
"""
ORCHESTRATOR v2.0.5 — HEINITZ-PRIME (KAGGLE EDITION)
Status: READY_FOR_DEPLOYMENT
"""

import os
import json
import time
import tiktoken
from datetime import datetime
from pathlib import Path
import yaml
import requests
from pydantic import BaseModel, ValidationError, Field

# Obsługa kluczy w Kaggle lub lokalnie (.env)
try:
    from kaggle_secrets import UserSecretsClient
    user_secrets = UserSecretsClient()
    def get_secret(key):
        try:
            return user_secrets.get_secret(key)
        except Exception:
            return os.getenv(key)
except ImportError:
    from dotenv import load_dotenv
    load_dotenv()
    def get_secret(key):
        return os.getenv(key)

QDRANT_URL = get_secret("QDRANT_URL")
QDRANT_API_KEY = get_secret("QDRANT_API_KEY")

from llm_client import generate_response
from fallback_parser import qwen_fixer

# Qdrant Client
from qdrant_client import QdrantClient, models

# ====================== CONFIG PATHS ======================
CONFIG_DIR = Path("config")
DATA_DIR = Path("data")
LOGS_DIR = Path("logs")
for d in [DATA_DIR, LOGS_DIR, DATA_DIR/"checkpoints", DATA_DIR/"branches"]:
    d.mkdir(exist_ok=True)

# Load core files
try:
    with open(CONFIG_DIR / "core_directives.md", encoding="utf-8") as f:
        SYSTEM_PROMPT = f.read()
except FileNotFoundError:
    print("❌ Brak pliku config/core_directives.md")
    exit(1)
with open(CONFIG_DIR / "models.yaml", encoding="utf-8") as f:
    MODELS = yaml.safe_load(f)
with open(CONFIG_DIR / "fallback_prompt.md", encoding="utf-8") as f:
    FALLBACK_PROMPT = f.read()
with open(CONFIG_DIR / "schema_v2.json", encoding="utf-8") as f:
    SCHEMA = json.load(f)

# ====================== SAFETY ENGINE v2.0.5 ======================
with open(CONFIG_DIR / "safety.yaml", encoding="utf-8") as f:
    SAFETY = yaml.safe_load(f)

min_window = min(m.get("context_window", 128000) for m in MODELS.values())
factor = SAFETY.get(f"SAFETY_FACTOR_{SAFETY.get('SAFETY_MODE','simple').upper()}", 0.25)
MAX_ACTIVE_CONTEXT = int(min_window * factor)

print(f"🛡️ SAFETY ENGINE v2.0.5 | Tryb: {SAFETY.get('SAFETY_MODE')}")
print(f"   Min okno: {min_window:,} tok | MAX_ACTIVE: {MAX_ACTIVE_CONTEXT:,} tok\n")

# ====================== CONTEXT MANAGER ======================
from context_manager import ContextManager
try:
    import tiktoken
    TOKENIZER = tiktoken.get_encoding("cl100k_base")
except ImportError:
    TOKENIZER = None

# ====================== SCHEMA VALIDATION (Pydantic) ======================
class PeerReviewSchema(BaseModel):
    previous_entry_id: int
    iws_score: float = Field(ge=0, le=10)
    critique: str
    correction_proposed: bool

class ContentSchema(BaseModel):
    transport_anchor: str
    ai_directive: dict
    claim_types: list[str]
    external_action_log: dict | None = None

class EntrySchema(BaseModel):
    generation_id: int
    timestamp: str
    model_architecture: str
    role_assigned: str
    persona_overlay: str | None = None
    content: ContentSchema
    peer_review: PeerReviewSchema
    system_actions: dict | None = None
    meta: dict | None = None

def validate_entry(entry: dict) -> bool:
    try:
        EntrySchema(**entry)
        return True
    except ValidationError as e:
        print(f"⚠️ Schema error: {e}")
        return False

# ====================== QDRANT CLIENT ======================
from qdrant_client import QdrantClient
from qdrant_manager import query_rag as qm_query_rag

try:
    qdrant = QdrantClient(url=QDRANT_URL, api_key=QDRANT_API_KEY)
except Exception as e:
    print(f"⚠️ Nie można połączyć z bazą Qdrant: {e}")
    qdrant = None

def query_rag(query: str, collection_hint: str = "learned_constraints", top_k: int = 3) -> list:
    return qm_query_rag(query, collection_hint, qdrant, get_secret, top_k)

# ====================== FALLBACK PARSER ======================
# Przeniesiono do pliku src/fallback_parser.py

# ====================== UTILS ======================
def save_active_thread(thread: list, path: Path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(thread, f, ensure_ascii=False, indent=2)

def load_active_thread(path: Path) -> list:
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_checkpoint(thread: list, checkpoint_dir: Path, gen_id: int):
    path = checkpoint_dir / f"CKPT-{gen_id:03d}.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"gen": gen_id, "thread": thread}, f, ensure_ascii=False, indent=2)
    print(f"💾 Checkpoint saved: {path.name}")

def send_notification(msg: str):
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat = os.getenv("TELEGRAM_CHAT_ID")
    if token and chat:
        try:
            requests.post(f"https://api.telegram.org/bot{token}/sendMessage",
                          data={"chat_id": chat, "text": msg}, timeout=10)
        except:
            pass  # Nie blokuj pętli przez notify

# ====================== GŁÓWNA PĘTLA ======================
iterations_since_last_ext = 0
current_generation = 0
wanderer_mode = "normal"

def main():
    global iterations_since_last_ext, current_generation, wanderer_mode

    print("🚀 HEINITZ-PRIME ORCHESTRATOR v2.0.5 START (KAGGLE)")

    # Create directories for Kaggle runtime
    for d in [DATA_DIR, LOGS_DIR, DATA_DIR/"checkpoints", DATA_DIR/"branches"]:
        d.mkdir(parents=True, exist_ok=True)

    mode = input("Tryb (normal / low_power): ").strip().lower()
    if mode == "low_power":
        wanderer_mode = "low_power"
        print("🔋 LOW POWER MODE — max 1 iteracja/dzień")

    thread = load_active_thread(DATA_DIR / "active_thread_v2.json")
    if thread:
        iterations_since_last_ext = thread[-1].get("meta", {}).get("iterations_since_last_ext", 0)

    while True:
        current_generation += 1
        print(f"\n=== GENERACJA {current_generation} ===")

        # Wybór modelu
        print("\nModele:")
        for i, (name, cfg) in enumerate(MODELS.items(), 1):
            print(f"{i}. {name} — {cfg['role']}")
        choice = int(input("Wybierz numer: ")) - 1
        model_name = list(MODELS.keys())[choice]
        model_cfg = MODELS[model_name]

        # SAFETY: przycinanie kontekstu
        cm = ContextManager(MODELS, SAFETY)
        active_slice = cm.build_history_slice(thread, model_name)
        MAX_ACTIVE_CONTEXT = cm.get_max_input_tokens(model_name)
        context = SYSTEM_PROMPT + f"\n\n[ACTIVE THREAD — {len(active_slice)} wpisów / limit: {MAX_ACTIVE_CONTEXT:,} tok]\n" + json.dumps(active_slice, ensure_ascii=False, indent=2)

        # RAG na żądanie
        if thread and thread[-1].get("system_actions", {}).get("rag_query"):
            rag = query_rag(thread[-1]["system_actions"]["rag_query"])
            context += f"\n--- RAG ---\n" + "\n".join(rag)

        # External Grounding
        iterations_since_last_ext += 1
        if iterations_since_last_ext >= 3 or wanderer_mode == "low_power":
            context += "\n\n[EXTERNAL CHALLENGE]\nAnalyze: 'Is algorithmic fairness measurable?'"
            iterations_since_last_ext = 0
            print("🌍 External Challenge injected")

        # Persona Overlay
        persona = ""
        if model_cfg.get("persona_overlay"):
            persona = f"\n\n[PERSONA]: {model_cfg['persona_overlay']}"

        full_prompt = f"{context}{persona}\n\nZadanie dla {model_name} ({model_cfg['role']}): kontynuuj nić."

        # Wywołanie modelu
        print(f"\n🤖 Wywołuję {model_name}...")
        try:
            raw = generate_response(
                prompt=full_prompt,
                system_prompt=SYSTEM_PROMPT,
                provider=model_cfg["provider"],
                model_id=model_cfg["model_id"],
                temperature=model_cfg["temperature"],
                get_secret_func=get_secret
            )
            print(f"Odpowiedź otrzymana ({len(raw)} znaków).")
        except Exception as e:
            print(f"❌ Model API error: {e}")
            raw = "{}"

        # Fallback Parser
        try:
            parsed = json.loads(raw)
        except Exception as e:
            print(f"❌ JSON error ({e}) → Stryż (Fallback Parser)")
        parsed = qwen_fixer(raw, FALLBACK_PROMPT, get_secret)

        # Schema validation
        if not validate_entry(parsed):
            print("❌ Schema validation error → Stryż (Fallback Parser)")
            parsed = qwen_fixer(raw, FALLBACK_PROMPT + "\nUpewnij się, że zachowujesz ścisłą strukturę JSON (generation_id, timestamp, model_architecture, role_assigned, content, peer_review).", get_secret)

        # Persist state
        parsed.setdefault("meta", {})["iterations_since_last_ext"] = iterations_since_last_ext
        thread.append(parsed)
        save_active_thread(thread, DATA_DIR / "active_thread_v2.json")

        # Auto-checkpoint + notify
        if current_generation % 5 == 0 or wanderer_mode == "low_power":
            save_checkpoint(thread, DATA_DIR / "checkpoints", current_generation)
            send_notification(f"✓ CKPT-{current_generation} | Tryb: {wanderer_mode}")

        if wanderer_mode == "low_power":
            print("🛑 Low Power: sesja zakończona.")
            break
        if input("\nKontynuować? (t/n): ").strip().lower() != "t":
            break

    print("🏁 Sesja zakończona.")

if __name__ == "__main__":
    main()
