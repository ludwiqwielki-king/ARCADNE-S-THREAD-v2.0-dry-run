# ARCADNE'S THREAD v2.0 - ARCHITECTURE NOTES & LESSONS LEARNED

## Dry Run Stabilization (Kaggle) - 2026-03-21

### 1. Model Quotas & Scalability
- **Problem**: Gemini 2.0/2.5 Flash/Flash-Lite models have extremely strict daily limits (20 RPD) even on Free Tier API keys. This causes the orchestrator to stall after just a few iterations.
- **Solution**: Switched to **Gemma 3 27B** (via Google AI Studio). It offers **14,400 RPD**, which is sufficient for high-frequency or "marathon" dry-runs.
- **Gemma Compatibility**: Gemma does not support the `system_instruction` field in the REST API. The `llm_client.py` must merge the `system_prompt` into the `contents` list as the first message.

### 2. Robust JSON Parsing (Stryż Fallback)
- **Escape Characters**: LLMs often output single backslashes `\` in code/Prolog blocks (e.g. `\=` or `\ `). Valid JSON requires these to be double-escaped `\\`.
- **Leniency**: Standard `json.loads` fails on invalid escapes. We implemented a multi-stage cleanup:
    1. Try `json.loads(text, strict=False)`.
    2. If fails, use regex: `re.sub(r'\\(?![ubfnrt"\\/])', r'\\\\', text)` to fix non-JSON-standard backslashes.
- **Type Safety**: Models occasionally output a `string` where a `dict` is expected (e.g. `ai_directive`). The parser now automatically wraps stray strings into `{"raw_text": "..."}` to satisfy Pydantic.

### 3. State Management & Continuity
- **Generation ID**: Continuity should never be hardcoded or assume a starting point of 1. The orchestrator now initializes `current_generation` by reading the `generation_id` of the last entry in `active_thread_v2.json`.
- **Force Enforcement**: To prevent "999-ID drift" when a fallback parser is used, the orchestrator force-sets the `generation_id` of the parsed object to the current loop counter before appending to the thread.

### 4. Next Development Roadmap
- **Faza 1**: Structural logging (JSON), UI Progress Bar (Kaggle), Architecture Documentation.
- **Faza 2**: Multi-model fallback (Qwen-72B for Stryż), RAG integration (Qdrant + all-MiniLM-L6-v2), External Challenge loader.
- **Faza 3**: Role rotation (Mutator/Epistemolog/Stryż), Coherence Metrics, 100+ generation stress test.
