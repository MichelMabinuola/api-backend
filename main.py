from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, AsyncGenerator, Literal
import json
import logging
from datetime import datetime
from sys_prompt import SYSTEM_PROMPT
import sys
from openai import AsyncOpenAI
from read_kb import read_knowledge_base
import os
from dotenv import load_dotenv
import uvicorn

# -------------------- Logging --------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

# -------------------- Environment --------------------
load_dotenv(".env")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = AsyncOpenAI(api_key=OPENAI_API_KEY)

# -------------------- Knowledge Base --------------------
knowledge_base = read_knowledge_base()
FORMATTED_SYSTEM_PROMPT = SYSTEM_PROMPT.format(context=knowledge_base)

logger.info(f"Knowledge base loaded ({len(knowledge_base)} chars)")

# -------------------- FastAPI App --------------------
app = FastAPI(title="Michael's Portfolio AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------- Models --------------------
class Message(BaseModel):
    role: Literal["system", "user", "assistant", "tool", "function", "developer"]
    content: str


class ChatRequest(BaseModel):
    message: str
    history: Optional[List[Message]] = Field(default_factory=list)


# -------------------- Streaming LLM --------------------
async def stream_response(query: str,history: Optional[List[Message]] = None) -> AsyncGenerator[str, None]:
    try:
        messages = [{"role": "system", "content": FORMATTED_SYSTEM_PROMPT}]

        if history:
            for msg in history[-6:]:  # Limit memory
                messages.append({"role": msg.role, "content": msg.content})

        messages.append({"role": "user", "content": query})
        stream = await client.chat.completions.create(
            model="gpt-5.2",
            messages=messages,
            max_completion_tokens=500,
            stream=True,
            temperature=0.3
        )
        
        async for chunk in stream:
            if chunk.choices:
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield f"data: {delta.content}\n\n"

        yield "data: [DONE]\n\n"

    except Exception as e:
        logger.error(f"Streaming error: {str(e)}")
        error_data = json.dumps({"error": "Something went wrong. Please try again."})
        yield f"data: {error_data}\n\n"
        yield "data: [DONE]\n\n"


# -------------------- Endpoints --------------------
@app.get("/")
async def root():
    return {
        "status": "online",
        "message": "Michael's Portfolio AI Assistant is running",
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/chat")
async def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")


    return StreamingResponse(
        stream_response(request.message, request.history),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )



