
from fastapi import APIRouter, HTTPException,status

from backend.models.py_models import ChatRequest, ChatResponse
from backend.llm.llm_client import LLMService
llm = LLMService()
router = APIRouter()

@router.post("/chat",status_code=status.HTTP_200_OK)
async def chat_endpoint(request: str) -> str:
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

        return ChatResponse(reply=reply)


    except HTTPException:
        # Re-raise intentional HTTPExceptions without catching them below
        raise

    except Exception as e:
        # Log the full stack trace on your server, but hide internal details from the user
       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating a response."
        ) from e