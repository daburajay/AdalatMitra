# AdalatMitra — Project Notes

**Last updated:** 2026-06-19
**Purpose:** Reference doc for architecture, decisions, and environment setup so progress isn't lost across sessions.

---

## 1. What this project is

AI Court Companion App for India. Common litigants enter a case number/party name and get:
- Real-time case status from eCourts (via `bharat-courts` library)
- A plain-language explanation of what's happening (Hindi/Hinglish/English/regional)
- WhatsApp reminders (future)
- "Second opinion" sanity-check on case progress (future)

Target users: common litigants in Tier 2/3 cities with low legal literacy.

---

## 2. Environment setup

- **OS:** Windows
- **Project path:** `D:\Python\AdalatMitra`
- **Python:** 3.13 (confirmed via `py -0`)
- **Virtual env name:** `vamt`
  ```bash
  vamt\Scripts\activate
  ```
- **Key installed packages:**
  ```bash
  pip install streamlit
  pip install bharat-courts[all]      # court data — NOT the old 'ecourts' package (broken/deprecated)
  pip install python-dotenv requests
  ```

### `.env` file (project root)
```
HF_TOKEN=hf_xxxxxxxxxxxxx          # HuggingFace token — needed for ONNXCaptchaSolver model download
ANTHROPIC_API_KEY=sk-ant-xxxxxxxx  # for explanation_agent (Claude)
GEMINI_API_KEY=                    # to be added — primary LLM per ai_gateway design
GROQ_API_KEY=                      # to be added — fallback LLM
```

---

## 3. Critical library notes (don't repeat these mistakes)

- ❌ `pip install ecourts` → wrong/broken package, import fails (`from ecourts import ECourt` does NOT work)
- ✅ `pip install bharat-courts[all]` is correct (or `[ocr]` / `[onnx]` for lighter installs)
- The OCR captcha solver (`ddddocr`) has **no Python 3.13 build** — use ONNX instead:
  ```python
  from bharat_courts.captcha.onnx import ONNXCaptchaSolver   # capital ONNX, not Onnx
  ```
- `ONNXCaptchaSolver` needs a **HuggingFace token** (`HF_TOKEN` in `.env`) to download its model on first run. Without it: `RuntimeError: HuggingFace requires authentication...`
- As of last test, the default HuggingFace model URL the library tries (`thelou1s/captchabreaker`) returned **404** — auto-solving is currently broken. **Working fallback: manual CAPTCHA solver** — saves image to `captcha_temp.png`, you read it and type the answer into a Streamlit text input / terminal prompt.
- `client.list_case_types(court)` returns a **dict** (`{id: name}`), not a list of objects — don't call `.id` / `.name` on its items directly.
- Court codes used so far: `delhi`, `bombay`, `madras`, `allahabad`, `calcutta`, `karnataka`, `kerala`, `gujarat`.
- CNR format: `DLHC010964712024` (court code + case number + year, 16 chars).
- Confirmed working end-to-end: party name search → real case list (e.g. "Union of India" 2024 → 2287 live Delhi HC cases) → CNR + petitioner/respondent returned correctly.
- Case-by-case-number search needs the **correct `case_type` ID** matched to the case — don't just default to the first case type in the dict, match by name (e.g. "LA.APP." vs "ARB.A.").

---

## 4. Architecture (locked — don't deviate without reason)

Clean Architecture, top to bottom:
```
UI Layer        → streamlit_app.py, pages/, components/
Controller       → ui_manager.py, query_router.py
Agent Layer      → case_agent, order_agent, timeline_agent,
                    explanation_agent, advice_agent, translation_agent, pdf_agent
Service Layer    → bharat_court_service.py, pdf_service.py,
                    ai_gateway.py, gemini_service.py, groq_service.py
External APIs    → eCourts (via bharat-courts), Gemini, Groq
```

### Folder structure
```
AdalatMitra/
├── frontend/
│   ├── streamlit_app.py
│   ├── ui_manager.py
│   ├── pages/
│   │   ├── home_page.py
│   │   ├── case_dashboard.py
│   │   └── pdf_page.py
│   ├── components/
│   │   ├── chat_box.py
│   │   ├── case_card.py
│   │   ├── timeline_view.py
│   │   ├── order_card.py
│   │   ├── sidebar.py
│   │   └── suggestion_buttons.py
│   └── styles/
│       └── custom_css.py
├── agents/
│   ├── query_router.py
│   ├── case_agent.py
│   ├── order_agent.py
│   ├── timeline_agent.py
│   ├── explanation_agent.py
│   ├── advice_agent.py
│   ├── translation_agent.py
│   └── pdf_agent.py
├── services/
│   ├── bharat_court_service.py
│   ├── pdf_service.py
│   ├── ai_gateway.py
│   ├── gemini_service.py
│   └── groq_service.py
├── models/
│   ├── case_model.py
│   ├── order_model.py
│   └── timeline_model.py
├── state/
│   └── session_state.py
├── prompts/
│   ├── explanation_prompt.py
│   ├── advice_prompt.py
│   ├── translation_prompt.py
│   └── summary_prompt.py
├── utils/
│   ├── logger.py
│   ├── helpers.py
│   └── constants.py
└── data/
    ├── uploaded_pdfs/
    ├── temp/
    └── cache/
```

### Design principles
- No file should exceed ~200 lines. If `streamlit_app.py` is growing past that, split into `components/`.
- No agent calls Gemini/Groq directly — everything routes through `ai_gateway.py` (single LLM entry point, Gemini primary → Groq fallback, silent to the user).
- LangGraph + Qdrant (RAG) are **future** additions — not in current MVP scope.

---

## 5. Build order (5 phases — don't skip ahead)

| Phase | What | Status |
|---|---|---|
| 1 | Skeleton — all folders + empty/stub files, `models/`, `state/session_state.py` | Not started |
| 2 | Data layer — `bharat_court_service.py` + `case_agent.py`, tested in isolation | **Proven working manually** (see §3) — needs to be formalized into service/agent split |
| 3 | AI gateway — `ai_gateway.py` (Gemini primary, Groq fallback) + `explanation_agent.py` | Partial — `explanation_agent.py` built using Anthropic API directly; needs Gemini/Groq gateway wrapper |
| 4 | Router — `query_router.py`, detects intent, dispatches to agents | Not started |
| 5 | Modular UI — `streamlit_app.py` + `components/` | Partial — built single-file prototype with session_state, CAPTCHA UI, language selector; needs splitting into components per architecture |

---

## 6. Runtime trace (target flow for "case status" query)

```
User → streamlit_app.py → query_router.py → case_agent.py
     → bharat_court_service.py (bharat-courts lib) → live case data
     → timeline_agent.py → explanation_agent.py
     → ai_gateway.py (Gemini → fallback Groq) → translation_agent.py
     → Streamlit UI response
```

---

## 7. Open decisions / TODO

- [ ] Get Gemini + Groq API keys, build `ai_gateway.py`, `gemini_service.py`, `groq_service.py`
- [ ] Decide: keep Anthropic-based `explanation_agent.py` or fully migrate to Gemini/Groq per original design
- [ ] Fix CAPTCHA auto-solve (HuggingFace 404) — or commit to manual CAPTCHA-in-UI as the permanent approach for MVP
- [ ] Build `query_router.py` intent detection (case status / explain order / legal advice / PDF upload)
- [ ] Split current single-file Streamlit prototype into `frontend/components/`
- [ ] PDF flow (`pdf_agent.py`, classification, case info extraction) — not started
- [ ] Translation agent — currently folded into explanation_agent's language param; may need to split per architecture doc
- [ ] WhatsApp reminders — not started, post-MVP
- [ ] RAG (Qdrant + judgments/bare acts) — explicitly future scope, not MVP

---

## 8. Useful commands

```bash
# Activate environment
vamt\Scripts\activate

# Run the app
streamlit run app.py          # current prototype name — will move to frontend/streamlit_app.py

# Test court data fetch directly
python agents/testp.py
```

---

*This file is a working memory aid — update it after each significant session so context isn't lost between conversations.*
