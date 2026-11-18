
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


@router.post("/chat",status_code=status.HTTP_200_OK,response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest) -> StreamingResponse:
    try:
        # Use the most recent user message as the question for RAG and the model
        question = next(
            (m.content for m in reversed(request.messages) if m.role == "user"),
            None,
        )
        if not question:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No user message found.",
            )

        
        # FastAPI runs it in a worker thread, so the server stays responsive.
        reply = llm.generate_text(question)

        if not reply or not reply.strip():
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Received an empty response from the AI service.",
            )

        return StreamingResponse(
            llm.generate_text(question),
            media_type="text/plain",
        )


    except HTTPException:
        # Re-raise intentional HTTPExceptions without catching them below
        raise

    except Exception as e:
        # Log the full stack trace on your server, but hide internal details from the user
        logger.exception('Interaction failed')
        raise HTTPException(
            
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating a response."
        ) from e