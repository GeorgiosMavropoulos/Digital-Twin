
from fastapi import APIRouter, HTTPException,status
from fastapi.responses import StreamingResponse
from backend.models.py_models import ChatResponse, ChatRequest
from backend.llm.llm_client import LLMService
llm = LLMService()
router = APIRouter()
import logging
import sys

from fastapi import FastAPI

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("digital_twin")



@router.post("/chat", status_code=status.HTTP_200_OK)
async def chat_endpoint(request: ChatRequest) -> StreamingResponse:
    question = next(
        (m.content for m in reversed(request.messages) if m.role == "user"),
        None,
    )
    if not question or not question.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No user message found.",
        )

    stream = llm.generate_text(question)  # όνομα όπως στο LLMService
    return StreamingResponse(stream, media_type="text/plain")