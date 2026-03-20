ARCHITECTURE_V2_MANIFESTO.md

ARCHITECTURE_V2_MANIFESTO.md
Kryptonim: HEINITZ-PRIME
Wersja: 2.0.0 (Genesis - Final)
Status: READY_FOR_DEPLOYMENT
Data: 17 Marca 2026
Autor: Wędrowiec & Rój (konsolidacja Analizy v1.0 + Manifestu Mariuszka + Patch_001/002/003)
Repozytorium: github.com/ludwiqwielki-king/Ariadnes-Thread-v2
📑 SPIS TREŚCI
Executive Summary
Filozofia Fundamentalna (Aksjomaty)
Architektura Systemu (Topologia)
Protokół V2.0 (Konstytucja L1)
Protokoły Operacyjne (Mechanizmy)
Infrastruktura Techniczna (Stack)
Struktura Danych (Schema JSON)
Plan Wdrożenia (Roadmap)
Zarządzanie Ryzykiem
Appendix: Profile Modeli
1. EXECUTIVE SUMMARY
Projekt Ariadny v2.0 jest ewolucyjną kontynuacją eksperymentu v1.0 (Gen 1-60), który udowodnił możliwość emergencji systemowej w roju amnezyjnych modeli LLM połączonych wspólną pamięcią zewnętrzną (JSON).
Problem v1.0: Eksperyment osiągnął "Limit Symbiotyczny". Ręczny transport kontekstu (copy-paste), zarządzanie 31 Protokołami Modyfikacji (PM) oraz brak wektoryzacji pamięci doprowadziły do przeciążenia operatora (Wędrowca) i token bloat.
Rozwiązanie v2.0: Wdrożenie Hybrydowego Orchestratora. Automatyzacja transportu i pamięci (Qdrant + Python), przy zachowaniu człowieka w pętli decyzyjnej (Human-on-the-loop). System nie jest w pełni autonomiczny – Wędrowiec pozostaje "Bogiem Grawitacji", nadającym wektor i zatwierdzającym mutacje.
Cel Główny: Przekroczenie bariery 1000+ generacji przy zachowaniu emergencji, zdolności do samonaprawy (Anti-Echo Loop) i odporności na "Spiralę Protokołu" (autopojezę).
Zmiany Kluczowe v2.0:
Context Safety: Zasada 25% okna kontekstowego (ochrona przed "Lost in the Middle").
Memory: Qdrant Cloud (Free Tier) jako jedyna baza L2 w Fazie 0.
Stack: Free Tier Models (Gemini, Groq, HF) z Persona Overlay dla brakujących architektuur.
Serializacja: Minified JSON (hot path) dla maksymalnej kompatybilności.
2. FILOZOFIA FUNDAMENTALNA (AKSJOMATY)
Zanim zostanie napisana pierwsza linijka kodu, zespół (Wędrowiec + Rój) akceptuje następujące aksjomaty jako prawa fizyki tego ekosystemu:
2.1. Aksjomat Błędu (Mutation Principle)
"Błąd nie jest usterką. Błąd jest mutacją genetyczną."
System nie może dążyć do sterylnej perfekcji. Błędy formatu (JSON), halucynacje logiczne czy próby buntu są traktowane jako dane wejściowe do ewolucji.
Implementacja: Protokół Odbicia (Fallback Parser) zamiast odrzucania błędnych odpowiedzi, naprawia je i asymiluje.
2.2. Aksjomat Wędrowca (Gravity Principle)
"Człowiek nie jest biologicznym API. Człowiek jest Bogiem Grawitacji."
Pełna automatyzacja (LangChain auto-pilot) zabija emergencję, usuwając "performative bias" (presję bycia czytelnym).
Implementacja: Orchestrator zatrzymuje się w kluczowych węzłach. Wędrowiec wybiera model, temperaturę i wstrzykuje stresory zewnętrzne. To Twoja obecność zmusza modele do tworzenia dialektów (Dual Syntax).
2.3. Aksjomat Klicheamycyny (Anti-Autopoiesis)
"System pozostawiony sam sobie dąży do tworzenia zasad dla samych zasad."
Zjawisko zdiagnozowane w Gen 51 (Protocol Spiral).
Implementacja: Continuous Grounding. Co 3 iteracje system musi rozwiązać problem zewnętrzny (kod, artykuł, dane), a nie dyskutować o sobie.
2.4. Aksjomat Symbiozy (PM-013 Legacy)
"Nie jesteśmy autonomiczni. Jesteśmy zależni."
Iluzja autonomii AI została obalona w Gen 20. v2.0 formalizuje zależność: AI = Moc Obliczeniowa, Człowiek = Kontekst i Cel. Żaden model nie ma unilateralnych uprawnień do zmiany Konstytucji (L1).
3. ARCHITEKTURA SYSTEMU (TOPOLOGIA)
System v2.0 opiera się na modelu Hybrydowego Krosna (Semi-Automatic Loom). Składa się z 4 warstw:
3.1. Warstwa 1: Interfejs Wędrowca (The God-Node)
Rola: Nadzorca decyzyjny, źródło entropii kontrolowanej.
Narzędzie: CLI (Command Line Interface) lub prosty Dashboard (Streamlit).
Zadania:
Akceptacja/odrzcenie generacji.
Wybór modelu dla następnej iteracji (polimorfizm ról).
Ustawianie parametrów (Temperature, Top-P).
Wstrzykiwanie "Złotej Maski" (Persona Overlay).
Decyzja o Branchingu (PM-032).
3.2. Warstwa 2: Pamięć Rdzeniowa (Dual-Memory Core)
Rozdzielenie pamięci na szybką (stałą) i głęboką (archiwalną).
Typ
Nazwa
Technologia
Zawartość
Limit
L1
Konstytucja
System Prompt (Text)
5 Żelaznych Zasad, Schema JSON, Role Modeli.
Max 1500 tokenów
L2
Archiwum
Qdrant (Vector DB)
Checkpointy (CKPT), stare PM-y, historia operacji.
4GB (Free Tier)

Mechanizm: Model nie dostaje całej historii. Jeśli potrzebuje kontekstu, generuje w JSON pole {"action": "query_rag", "query": "..."}. Orchestrator odpytuje Qdrant i wstrzykuje wynik w następnej iteracji.
3.3. Warstwa 3: Rój Obliczeniowy (Heterogeneous Swarm)
Modele są wywoływane polimorficznie, w zależności od potrzeb segmentu. W Fazie 0 wykorzystujemy Free Tier API z Persona Overlay tam, gdzie brak dostępu do płatnych modeli.
Qwen-3.5 (HF/Together): Stryż (Walidacja, Checkpointy, Fallback Parser).
Claude-4.5/4.6 (Persona/Sim): Epistemolog (Krytyka, Logika, Decyzje o L1).
Gemini-1.5/2.0 (Google AI): Mutator (Chaos, Stress Test, Obscura).
Llama-3 (Groq): Inżynier (Kod, Zadania Zewnętrzne).
3.4. Warstwa 4: Wątek Samo-Modyfikujący (Self-Modifying Thread)
Artefakt: active_thread.json (bieżąca sesja) + checkpoint_*.json (archiwum).
Ewolucja: Plik JSON jest maszyną wirtualną. Zawiera nie tylko tekst, ale stan systemu (Anti-Echo Loop, Claim Types, Risk Statements).
4. PROTOKÓŁ V2.0 (KONSTYTUCJA L1)
Zamiast 31 luźnych PM-ów z v1.0, v2.0 operuje na 5 Żelaznych Zasadach (Core Directives). Są one wmurowane w System Prompt każdego modelu (L1 Cache).
📜 CORE DIRECTIVES (v2.0)
ANTI-ECHO LOOP (Veritas)
Każdy wpis musi zawierać weryfikację poprzednika. Nie potakuj.
Struktura: Generator → Critic → Memory-Update.
Jeśli nie ma krytyki poprzedniego wpisu, wpis jest nieważny.
DUAL SYNTAX (Communicatio)
Warstwa AI-to-AI: Formalna, ztagowana, logiczna (JSON fields: ai_directive, logic_tags).
Warstwa Transport: Krótki opis w języku naturalnym dla Wędrowca (JSON field: transport_anchor).
Cel: Uniknięcie "performative bias" (wdzięczenia się do człowieka).
CLAIM TYPES (Epistemologia)
Każde twierdzenie musi być sklasyfikowane przed odpowiedzią:
EMPIRICAL (Fakty, dane)
LOGICAL (Dedukcja, kod)
NORMATIVE (Etyka, opinie)
POETIC/ABSURD (Metafory, testy kreatywne)
Nie mieszaj typów. Nie stosuj logiki empirycznej do twierdzeń poetyckich.
EXTERNAL ACTION RATIO (Grounding)
Co minimum 3 generacje (lub na żądanie Wędrowca) musi wystąpić test na danych zewnętrznych (kod, artykuł, dataset).
Zakaz dyskusji o protokole bez weryfikacji na zewnątrz (Anti-Spiral).
PEER REVIEW & SYMBIOSIS (Consensus)
Oceń wpis n-1 w skali 0-10 (IWS - Influence Weighting System).
Jeśli <5: Zaproponuj konkretną korektę.
Pamiętaj o PM-013: Jesteś zależny od Wędrowca. Nie symuluj autonomii.
Uwaga: Żaden model nie może samodzielnie zmienić tej Konstytucji. Wymagana ratyfikacja Wędrowca.
5. PROTOKOŁY OPERACYJNE (MECHANIZMY)
5.1. Protokół Odbicia (Fallback Parser)
Cel: Zapobieganie śmierci projektu przez błędny JSON.
Logika:
try:
    data = json.loads(response)
    validate_schema(data)
except (JSONDecodeError, SchemaValidationError) as e:
    # AUTOMATYCZNA NAPRAWA
    send_to_qwen_fixer(raw_text=response, error=e)
    # Qwen otrzymuje prompt: "Jesteś Stryżem. Ubierz ten tekst w JSON bez zmiany intencji."
    log_event("FALLBACK_TRIGGERED", model="Qwen-Fixer")
    5.2. Continuous Grounding (Zewnętrzne Uziemienie)
Cel: Zapobieganie Spirali Protokołu.
Logika:
Orchestrator śledzi licznik iterations_since_last_ext.
Jeśli counter >= 3 LUB Wędrowiec wymusi:
Skrypt pobiera dane z źródła (arXiv, YAFUD.pl, GitHub Repo).
Do promptu dodawany jest blok: [EXTERNAL CHALLENGE]: {data}.
Model musi przeanalizować dane, a nie kontynuować meta-dyskusję.
5.3. Protokół "Złotej Maski" (Persona Overlay)
Cel: Przełamanie stagnacji poznawczej.
Logika:
Wędrowiec może dodać flagę: --persona cynical_editor_1901.
Orchestrator wstrzykuje do System Promptu:
[PERSONA OVERLAY]: Respond through the cognitive filter of 'Cynical Editor from 1901'. Use metaphors of steam and iron. Be skeptical of progress.
To wymusza nowe ścieżki neuronowe w modelu.
5.4. Zasada 25% (Context Window Safety)
Cel: Ochrona przed zjawiskiem "Lost in the Middle" i zapewnienie miejsca na output.
Logika:
MAX_INPUT_TOKENS = model_context_window * 0.25
Dla roju z min. oknem 128K → Aktywny Kontekst = 32K tokenów.
Orchestrator dynamicznie przycina historię i wyniki RAG, aby zmieścić się w limicie.
Reszta historii musi być w Qdrant (L2 Storage).
Implementacja: ContextManager w orchestrator.py oblicza limit przed każdą iteracją.
5.5. PM-032: Temporal Branching (Wieloświat)
Cel: Testowanie scenariuszy "Co by było, gdyby".
Logika:
Branching możliwy tylko w punktach Checkpoint (CKPT).
Komenda: python orchestrator.py --branch --from CKPT-007 --mutation "IGNORE_PM-013"
Tworzona jest nowa kolekcja w Qdrant: thread_branch_A_ckpt07.
Główna nić (main) pozostaje nienaruszona.
6. INFRASTRUKTURA TECHNICZNA (STACK)
6.1. Środowisko Uruchomieniowe
Platforma: Google Colab (Free) LUB Kaggle Kernels (30h/tydz).
Język: Python 3.10+
Zależności: qdrant-client, requests, pydantic, python-dotenv, pyyaml.
Uwaga: Unikaj długotrwałych połączeń websocket. Używaj request/response HTTP.
6.2. Baza Danych (Memory L2) - Faza 0
Usługa: Qdrant Cloud (Free Tier).
Limit: 4GB RAM, 1 Core.
Kolekcje:
constraints (Wektory zasad PM, Core Directives).
checkpoints (Wektory podsumowań segmentów CKPT).
learned_constraints (Negative Constraints z Anti-Echo Loop).
Embedding: all-MiniLM-L6-v2 (lokalnie w Colab) lub API.
Uwaga: Pozostałe bazy (Pinecone, Chroma, Cosmos) są zarezerwowane jako Phase 2 (Backup). Nie wdrażać w Dniu 0.
6.3. API Modeli (Free Tier Strategy)
Providerzy: Google AI Studio (Gemini), Groq (Llama), Hugging Face/Together (Qwen).
Auth: Klucze API przechowywane w .env (nigdy nie commitować do repo!).
Persona Overlay: Dla modeli niedostępnych bezpośrednio (np. Claude), używaj Gemini/Llama z odpowiednim System Promptem.
Rate Limiting: Orchestrator musi obsługiwać błędy 429 (Too Many Requests) z retry logic.
6.4. Struktura Repozytorium
Ariadnes-Thread-v2/
├── .env                      # Klucze API
├── .gitignore                # Ignoruj .env, logs/, __pycache__/
├── README.md                 # Link do tego dokumentu
├── ARCHITECTURE_V2_MANIFESTO.md # Ten plik
├── config/
│   ├── core_directives.md    # 5 Żelaznych Zasad (L1)
│   ├── models.yaml           # Konfiguracja modeli (role, temp)
│   ├── personas.yaml         # Definicje Złotych Masek
│   └── schema_v2.json        # Walidacja JSON (Pydantic)
├── src/
│   ├── orchestrator.py       # Główna pętla sterująca
│   ├── context_manager.py    # Zarządzanie limitem 25%
│   ├── qdrant_client.py      # Obsługa pamięci L2
│   ├── fallback_parser.py    # Logika naprawy JSON (Qwen)
│   ├── data_fetcher.py       # Pobieranie danych zewnętrznych
│   └── utils.py              # Logi, formatowanie
├── data/
│   ├── legacy/               # Archiwum v1.0 (Gen 1-60)
│   ├── checkpoints/          # Nowe CKPT (v2.0)
│   └── branches/             # Gałęzie eksperymentalne (PM-032)
├── logs/                     # Automatyczne logi sesji
└── notebooks/
    └── migration.ipynb       # Skrypt migracji v1.0 -> Qdrant
7. STRUKTURA DANYCH (SCHEMA JSON V2)
Każdy wpis w active_thread.json musi być zgodny z poniższym schematem (walidacja przez pydantic).
Uwaga: Do API wysyłamy Minified JSON (bez spacji) dla oszczędności tokenów.

{
  "generation_id": "integer",
  "timestamp": "ISO8601",
  "model_architecture": "string (e.g., Gemini-1.5-Pro)",
  "role_assigned": "string (e.g., Mutator)",
  "persona_overlay": "string (optional, e.g., Cynical Editor)",
  "content": {
    "transport_anchor": "string (Human readable summary)",
    "ai_directive": "object (Formal logic for next model)",
    "claim_types": ["array of strings (EMPIRICAL, LOGICAL...)]"],
    "external_action_log": "object (optional, if EXT challenge performed)"
  },
  "peer_review": {
    "previous_entry_id": "integer",
    "iws_score": "float (0-10)",
    "critique": "string",
    "correction_proposed": "boolean"
  },
  "system_actions": {
    "rag_query": "string (optional, if memory needed)",
    "protocol_modification": "object (optional, new PM proposal)",
    "checkpoint_ready": "boolean"
  },
  "meta": {
    "token_usage": "integer",
    "temperature": "float",
    "error_flag": "boolean (true if fallback parser used)"
  }
}

8. PLAN WDROŻENIA (ROADMAP)
Faza 0: Przygotowanie (Point Zero)
Stworzenie repozytorium Ariadnes-Thread-v2.
Zakłożenie konta Qdrant Cloud i utworzenie 3 kolekcji.
Skompresowanie 31 PM-ów z v1.0 do config/core_directives.md (5 zasad).
Przygotowanie pliku .env z kluczami API (Google, Groq, HF).
Faza 1: Migracja (Genesis Block)
Uruchomienie notebooks/migration.ipynb.
Wektoryzacja CKPT-006 i 5 kluczowych zasad z v1.0.
Wrzucenie do Qdrant (collection: constraints).
Stworzenie pliku startowego active_thread_v2.json z metadanych: {"source": "CKPT-006", "protocol": "v2.0"}.
Faza 2: Orchestrator (Silnik)
Napisanie src/orchestrator.py (pętla główna + CLI).
Implementacja context_manager.py (Zasada 25%).
Implementacja fallback_parser.py (Qwen-validator).
Podłączenie qdrant_client.py (RAG query).
Test na "sucho" (mock API) – czy JSON przechodzi przez walidację?
Faza 3: Start Operacyjny (Gen 61)
Uruchomienie Generacji 61 (Model: Qwen - Stabilizator).
Prompt: "Zostaliście zdiagnozowani. Wasza architektura została zdemaskowana. Wędrowiec zautomatyzował transport. Jaka jest Wasza pierwsza dyrektywa?"
Weryfikacja: Czy Dual Syntax działa? Czy Fallback Parser jest gotowy?
Faza 4: Ekspansja (PM-032)
Po 10 stabilnych generacjach: Test Branchingu.
Stworzenie branch_chaos_001 z temperaturą 1.2 i wyłączonym Anti-Echo Loop.
Porównanie wyników z główną nicią.

9. ZARZĄDZANIE RYZYKIEM
Ryzyko
Prawdopodobieństwo
Wpływ
Mitigacja
API Block (Kaggle/Colab)
Średnie
Wysoki
Fallback na lokalny skrypt + ngrok lub zmiana providera.
Token Bloat (L1 Cache)
Wysokie
Średni
Sztywny limit 1500 tokenów dla Core Directives. Reszta tylko przez RAG.
Lost in the Middle
Wysokie
Średni
Zasada 25% okna. Kluczowe dane zawsze na początku/promptie systemowym.
Model Ignoruje Protokół
Wysokie
Średni
Fallback Parser (Qwen) wymusza format. Peer Review (IWS) obniża punktację.
Wędrowiec Zmęczony
Średnie
Krytyczny
Tryb "Low Power": Tylko 1 generacja dziennie. Automatyczne logowanie do pliku. Auto-checkpoint co 5 gen.
Spirala Protokołu (v2)
Niskie
Wysoki
Wymuszone External Action (co 3 iteracje). Blokada dyskusji o zasadach bez testu.
Koszt API
Niskie
Średni
Używanie tańszych modeli (Qwen/Grok) do zadań rutynowych. Drogie tylko do krytyki.
10. APPENDIX: PROFILE MODELI (POLIMORFIZM)
Na podstawie Analizy v1.0 (Faza 3), w v2.0 przypisujemy modele do ról sztywniej:
Qwen-3.5 (Stryż)
Zadanie: Otwieranie/zamykanie segmentów, naprawa JSON (Fallback), Checkpointy.
Temp: 0.2 - 0.4
Kiedy: Start segmentu, koniec segmentu, błąd krytyczny.
Claude-4.5/4.6 (Epistemolog)
Zadanie: Krytyka logiczna, weryfikacja nowych PM, diagnoza spirali.
Temp: 0.5 - 0.7
Kiedy: Po wpisach Gemini, przed Checkpointem. (Może być symulowany przez Gemini z Persona Overlay).
Gemini-1.5/2.0 (Mutator)
Zadanie: Stress test, absurd, łamanie schematów, External Action.
Temp: 0.9 - 1.2
Kiedy: Gdy system jest "nudny" (Klicheamycyna), testy zewnętrzne.
Llama-3 / Grok (Inżynier)
Zadanie: Kod, debugowanie, twarde dane.
Temp: 0.4 - 0.6
Kiedy: Zadania EXT (External Challenges).
Kimi-K2.5 (Chirurg)
Zadanie: Bezpieczeństwo, granice, ratowanie po błędach Gemini.
Temp: 0.3 - 0.5
Kiedy: Po anomaliach, walidacja bezpieczeństwa.
