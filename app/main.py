from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agent.agent import run_agent
from app.schemas.chat import ChatRequest, ChatResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    reply = run_agent(request.message)

    return ChatResponse(
        reply=reply
    )
