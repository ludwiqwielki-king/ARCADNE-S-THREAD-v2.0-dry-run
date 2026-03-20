# ARCADNE'S THREAD v2.0 (HEINITZ-PRIME)

**Projekt badawczy emergencji systemowej w roju amnezyjnych modeli LLM.**

---

## 🧭 KONTEKST PROJEKTU

### Cel
Projekt badawczy emergencji systemowej w roju amnezyjnych modeli LLM. Uruchamiany na **Kaggle** (nie lokalnie).

### Architektura (zgodnie z `ARCHITECTURE_V2_MANIFESTO.md`)
- **Human-on-the-loop**: Wędrowiec podejmuje decyzje, skrypt wykonuje logistykę.
- **Dual Memory**: L1 Cache (system prompt, 5 Core Directives) + L2 Storage (Qdrant RAG).
- **Safety Engine**: Zasada 25% okna kontekstowego (`MAX_ACTIVE_CONTEXT = min_window * 0.25`).
- **Fallback Parser**: Błędy JSON są naprawiane przez Qwen, nie odrzucane.
- **External Grounding**: Co 3 iteracje wymuszony test na danych zewnętrznych (PM-030).

### Role Modeli
| Model | Rola | Zadanie |
|-------|------|---------|
| Qwen | Stryż | Validator, naprawa JSON, checkpointy |
| Gemini | Mutator | Architekt chaosu, stress test |
| Claude | Epistemolog | Krytyka logiczna, decyzje o L1 |
| Kimi | Chirurg | Bezpieczeństwo, granice |

---

## 🖥️ ŚRODOWISKO URUCHOMIENIOWE: KAGGLE (KLUCZOWE!)

> ⚠️ **TEN PROJEKT JEST PRZEZNACZONY DO URUCHOMIENIA NA KAGGLE, NIE LOKALNIE.**

- **NIE używamy pliku `.env`**. Klucze API pobieramy przez `kaggle_secrets.UserSecretsClient()`.
- **NIE tworzymy katalogów lokalnie** – Kaggle robi to w runtime. Orchestrator musi mieć `mkdir(exist_ok=True)`.
- **Internet musi być włączony** w ustawieniach notebooka Kaggle.
- **Zależności instalujemy przez `!pip install`** w pierwszej komórce notebooka.

### Instalacja na Kaggle
```python
# Pierwsza komórka notebooka Kaggle
!pip install qdrant-client requests pydantic python-dotenv pyyaml tiktoken
```

### Konfiguracja Secrets (Kaggle UI)
Dodaj następujące klucze w **Kaggle Notebook → Settings → Secrets**:
- `QDRANT_URL`
- `QDRANT_API_KEY`
- `GOOGLE_API_KEY` (lub inne, w zależności od używanych modeli)

---

## 📜 ZASADY DLA AGENTA (NON-NEGOTIABLE)

1. **Nigdy nie automatyzuj decyzji Wędrowca.** Kod ma zatrzymać się i czekać na input przy wyborze modelu, temperatury, branchingu.
2. **Zachowaj Kaggle compatibility.** Nie wprowadzaj `.env`, nie zakładaj lokalnych ścieżek.
3. **Zgodność z Manifestem.** Każda zmiana w `orchestrator.py` musi być zgodna z `ARCHITECTURE_V2_MANIFESTO.md`.
4. **Minifikacja JSON.** Do API wysyłaj `json.dumps(..., separators=(',', ':'))` dla oszczędności tokenów.
5. **Bezpieczeństwo kluczy.** Nigdy nie hardkoduj API keys. Zawsze przez `UserSecretsClient`.

---

## 💬 KOMUNIKACJA Z WĘDROWCEM

- Jeśli napotkasz niejasność w Manifestie – **zapytaj, nie zgaduj**.
- Jeśli poprawka łamie zasadę Kaggle – **zasygnalizuj, nie implementuj**.
- Po każdej większej zmianie – **podsumuj, co zmieniłeś i dlaczego**.

---

## 📁 STRUKTURA PROJEKTU

```
ARCADNE-S-THREAD-v2.0/
├── README.md                    # Ten plik
├── ARCHITECTURE_V2_MANIFESTO.md # Pełny manifest projektu
├── .gitignore                   # Ignoruj .env, data/, logs/, __pycache__/
├── config/
│   ├── core_directives.md       # 5 Żelaznych Zasad (L1 Cache)
│   ├── models.yaml              # Konfiguracja modeli (role, temp)
│   ├── fallback_prompt.md       # Instrukcje dla Fallback Parser
│   ├── safety.yaml              # Safety Engine config
│   └── schema_v2.json           # Walidacja JSON (Pydantic)
├── src/
│   ├── orchestrator.py          # Główna pętla sterująca
│   ├── context_manager.py       # Zarządzanie limitem 25%
│   ├── qdrant_manager.py        # Obsługa pamięci L2 (RAG)
│   ├── fallback_parser.py       # Logika naprawy JSON (Qwen)
│   ├── llm_client.py            # Wrapper na API modeli
│   └── serializer.py            # Minifikacja JSON
├── data/                        # Tworzone w runtime (Kaggle)
│   ├── checkpoints/             # Auto-checkpointy co 5 gen
│   └── branches/                # Gałęzie eksperymentalne (PM-032)
├── logs/                        # Automatyczne logi sesji
└── notebooks/
    └── Kaggle_Dry_Run.ipynb     # Notebook do uruchomienia na Kaggle
```

---

## 🚀 SZYBKI START

1. **Forkuj repozytorium** na GitHub.
2. **Otwórz Kaggle** → Create New Notebook → Import z GitHub.
3. **Dodaj Secrets** w ustawieniach notebooka.
4. **Włącz Internet** w Settings.
5. **Uruchom komórki** po kolei.
6. **Czekaj na input Wędrowca** przy każdym wyborze modelu.

---

## 📚 DOKUMENTACJA

- [`ARCHITECTURE_V2_MANIFESTO.md`](./ARCHITECTURE_V2_MANIFESTO.md) – Pełny manifest i filozofia projektu
- [`KNOWLEDGE_BASE/`](./KNOWLEDGE_BASE/) – Historia eksperymentu v1.0 (Gen 1-60)
- [`config/core_directives.md`](./config/core_directives.md) – 5 Żelaznych Zasad

---

## ⚠️ ZAGROŻENIA

| Ryzyko | Prawdopodobieństwo | Mitigacja |
|--------|-------------------|-----------|
| API Block (Kaggle) | Średnie | Fallback na lokalny skrypt + ngrok |
| Token Bloat (L1 Cache) | Wysokie | Limit 1500 tokenów dla Core Directives |
| Lost in the Middle | Wysokie | Zasada 25% okna, kluczowe dane na początku |
| Spiral Protokołu | Niskie | Wymuszone External Action co 3 iteracje |

---

## 📜 LICENCJA

See [LICENSE](./LICENSE) file.

---

> **"Błąd nie jest usterką. Błąd jest mutacją genetyczną."**  
> — Aksjomat Błędu, ARCHITECTURE_V2_MANIFESTO.md
