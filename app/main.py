from fastapi import FastAPI

from app.llm.deepseek_client import chat_with_deepseek
from app.schemas.chat import ChatRequest, ChatResponse


app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = chat_with_deepseek(request.message)

    return ChatResponse(reply=reply)