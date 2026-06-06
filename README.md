# NEXUS — Voice Sports Agent 🎙️

> **Speak. Research. Respond. All in voice.**

A production-grade AI voice agent that lets you ask sports questions out loud and get spoken answers back — powered by a hierarchical multi-agent system under the hood.

**Live Demo:** [famous-salmiakki-506e70.netlify.app](https://famous-salmiakki-506e70.netlify.app)

---

## What It Does

You talk. The agent thinks. It talks back.

Under the hood, your voice triggers a full multi-agent research pipeline — not just a chatbot wrapper. A Supervisor routes your question to specialized agents that search the web in real time and craft a structured response, which is then converted back to speech and played in your browser.

```
🎤 Voice Input
      ↓
🔊 Groq Whisper  →  Speech-to-Text
      ↓
🧠 LangGraph Supervisor  →  routes to best agent
      ├── 🔍 Researcher Agent  →  Tavily web search
      └── ✍️  Writer Agent     →  formats the response
      ↓
🔈 gTTS  →  Text-to-Speech
      ↓
🔊 Voice Output (MP3 plays in browser)
```

---

## Architecture

This is a **hierarchical multi-agent system** built with LangGraph.

| Layer | Technology | Role |
|---|---|---|
| STT | Groq Whisper (`whisper-large-v3`) | Converts voice to text |
| Supervisor | LangGraph + Groq LLaMA 3.3 70B | Routes between agents |
| Researcher | Tavily Search | Real-time web search |
| Writer | Groq LLaMA 3.3 70B | Formats final response |
| Memory | LangGraph MemorySaver | Per-session conversation history |
| TTS | gTTS (Google Text-to-Speech) | Converts response to audio |
| API | FastAPI | Serves both `/chat` and `/voice-chat` endpoints |
| Frontend | Vanilla HTML/CSS/JS | Futuristic mic UI, deployed on Netlify |
| Backend | Render | Python 3.11.8, auto-deploys on push |

---

## Endpoints

### `GET /`
Health check.
```json
{ "message": "Sports Agent API is running" }
```

### `POST /chat`
Text-based chat with the agent.
```json
// Request
{ "message": "Who won the Champions League?", "session_id": "abc123" }

// Response
{ "response": "Real Madrid won the 2024 Champions League..." }
```

### `POST /voice-chat`
Voice-based chat. Accepts multipart/form-data.
```
audio     → audio file (webm/m4a/mp3)
session_id → string
```
Returns raw `audio/mpeg` bytes — plays directly in the browser.

---

## Tech Stack

- **LangGraph** — multi-agent orchestration with stateful graph
- **LangChain** — LLM integrations and message handling
- **Groq** — blazing fast LLaMA 3.3 70B inference + Whisper STT
- **Tavily** — real-time web search for sports data
- **FastAPI** — async Python API
- **gTTS** — text-to-speech conversion
- **MemorySaver** — in-memory conversation checkpointing per session
- **Render** — backend deployment
- **Netlify** — frontend deployment

---

## Project Structure

```
Voice_agent/
├── api.py          # FastAPI app — /chat and /voice-chat endpoints
├── graph.py        # LangGraph StateGraph — nodes, edges, routing logic
├── agents.py       # Researcher and Writer agent definitions
├── supervisor.py   # Supervisor node — routes between agents
├── state.py        # Shared state schema (TypedDict)
├── requirements.txt
└── runtime.txt     # Python 3.11.8
```

---

## Local Setup

**1. Clone the repo**
```bash
git clone https://github.com/MAGUIRE-GOATED/Voice_agent.git
cd Voice_agent
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables**
```bash
# .env
GROQ_API_KEY=your_groq_key
TAVILY_API_KEY=your_tavily_key
```

**4. Run the server**
```bash
uvicorn api:app --reload
```

**5. Test at** `http://127.0.0.1:8000/docs`

---

## How The Agent Routing Works

The Supervisor is the brain. Every message goes through it first.

```python
def route_supervisor(state: State):
    return state["next"]  # "researcher", "writer", or "FINISH"
```

- If it needs live data → **Researcher** fires Tavily search
- If it has the data and needs to format it → **Writer** crafts the response
- If the response is ready → **FINISH** → back to the API

The Researcher can loop back to the Supervisor after a tool call, allowing multi-hop research before the Writer gets involved.

---

## Deployment

**Backend (Render)**
- Build: `pip install -r requirements.txt`
- Start: `uvicorn api:app --host 0.0.0.0 --port 10000`
- Add env vars: `GROQ_API_KEY`, `TAVILY_API_KEY`

**Frontend (Netlify)**
- Drag and drop `index.html`
- Make sure fetch URL points to your Render service URL

---

## Related Projects

- [Flight Agent](https://github.com/MAGUIRE-GOATED/Flight_agent) — RAG over KLM baggage docs with BM25 + ChromaDB
- [Sports Agent](https://github.com/MAGUIRE-GOATED/SPORTS_AGENT) — the text-only predecessor to this project

---

Built by [Wali](https://github.com/MAGUIRE-GOATED) — first-year CS student at IIIT Delhi, building production AI agents.
