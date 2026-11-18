import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.genai import errors
from backend.tools.tool import Tools
from collections.abc import Iterator
from backend.vector_db.vec_db import ChromaDb
import logging



logger = logging.getLogger("digital_twin")

from backend.prompts.prompt_templates import PromptTemplates
chroma = ChromaDb()
prompt_ = PromptTemplates()
tool = Tools()
load_dotenv()
class LLMService:
    def __init__(self,  default_model: str = "gemini-3.5-flash-lite", system_instruction: str | None = None):
        """
        Initialize the Gemini client. 
        Falls back to the GEMINI_API_KEY environment variable if api_key is not passed.
        """
        self.default_model = default_model
        self.client = genai.Client()

        #store the pdf so the model can answer
        chroma.store_pdf_in_chroma("Profile.pdf")
        
        config = types.GenerateContentConfig(
            system_instruction=system_instruction,
            tools=[tool.save_emails_schema],
        )

        # Initialize the chat ONCE so history persists across generate_text() calls
        self.chat = self.client.chats.create(
            model=self.default_model,
            config=config
        )

    def generate_text(self, question: str,) -> Iterator[str]:      
       
        """Yields text chunks as the model generates them."""
        try:
            relevant_context = chroma.retrieve_from_chroma(question)
            prompt = prompt_.digital_twin_prompt(
                profile_text=relevant_context,
                question=question,
            )

            message = prompt
            while True:
                function_calls = []

                for chunk in self.chat.send_message_stream(message=message):
                    if chunk.function_calls:
                        function_calls.extend(chunk.function_calls)
                    if chunk.text:
                        yield chunk.text

                # No tool calls means the answer is complete
                if not function_calls:
                    break

                tool_responses = []
                for call in function_calls:
                    result = tool.execute(call.name, call.args)
                    tool_responses.append(
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": result},
                        )
                    )
                message = tool_responses

        except errors.APIError as e:
            if e.code == 429:
                logger.exception(f"[API Rate Limit]: {e.message}")
                yield  "I am currently receiving too many requests. Please try again in a moment."
            elif e.code in (400, 404):
                logger.exception(f"[API Client Error {e.code}]: {e.message}")
                yield  "There was a configuration issue while processing your request."
            elif e.code in (500, 503):
                logger.exception(f"[API Server Error {e.code}]: {e.message}")
                yield  "The AI service is temporarily unavailable. Please try again shortly."
            else:
                logger.exception(f"[API Error {e.code}]: {e.message}")
                yield  "An unexpected service error occurred."

        except (ConnectionError, TimeoutError) as e:
            logger.exception(f"Chat handler failed: {e}")
            yield  "Network connection issue. Please check your internet and try again."

        except Exception as e:
            logger.exception(f"Chat handler failed: {e}")
            yield  "An internal error occurred. Please try again."



    
   
