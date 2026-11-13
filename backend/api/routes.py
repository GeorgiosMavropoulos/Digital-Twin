
from fastapi import APIRouter, HTTPException,status


from backend.llm.llm_client import LLMService
llm = LLMService()
router = APIRouter()

@router.post("/chat",status_code=status.HTTP_200_OK)
async def chat_endpoint(request: str) -> str:
    try:
        messages = [msg.model_dump() for msg in request.messages]

        # Enforce a 30-second timeout so hung LLM requests don't freeze workers
        reply = await llm.generate_text(messages)
        

        if not reply or not isinstance(reply, str):
            
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Received an invalid response from the AI service."
            )

        return reply


    except HTTPException:
        # Re-raise intentional HTTPExceptions without catching them below
        raise

    except Exception as e:
        # Log the full stack trace on your server, but hide internal details from the user
       
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while generating a response."
        ) from e