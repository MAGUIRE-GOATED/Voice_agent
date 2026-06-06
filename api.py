from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from groq import Groq
from elevenlabs.client import ElevenLabs
from graph import graph
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://famous-salmiakki-506e70.netlify.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── existing endpoints ──────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/")
def root():
    return {"message": "Sports Agent API is running"}

@app.post("/chat")
async def chat(request: ChatRequest):
    config = {"configurable": {"thread_id": request.session_id}}
    result = await graph.ainvoke({
        "messages": [HumanMessage(content=request.message)]
    }, config=config)
    response = result["messages"][-1].content
    return {"response": response}

# ── new voice endpoint ──────────────────────────────────────────

@app.post("/voice-chat")
async def voice_chat(audio: UploadFile = File(...), session_id: str = Form(...)):

    # STEP 1: Whisper STT — audio bytes → text
    groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    audio_bytes = await audio.read()
    transcription = groq_client.audio.transcriptions.create(
        file=(audio.filename or "audio.webm", audio_bytes),
        model="whisper-large-v3",
    )
    user_text = transcription.text

    # STEP 2: graph.ainvoke — same as /chat
    config = {"configurable": {"thread_id": session_id}}
    result = await graph.ainvoke(
        {"messages": [HumanMessage(content=user_text)]},
        config=config
    )
    response_text = result["messages"][-1].content

    # STEP 3: ElevenLabs TTS — text → audio bytes
    el_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
    audio_stream = el_client.text_to_speech.convert(
        text=response_text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_data = b"".join(audio_stream)

    # STEP 4: Return audio back to frontend
    return Response(content=audio_data, media_type="audio/mpeg")