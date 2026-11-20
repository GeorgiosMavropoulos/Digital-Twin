import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.genai import errors
from backend.tools.tool import Tools
from collections.abc import Iterator
from backend.vector_db.vec_db import ChromaDb
import logging
import httpx



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

    """
    def judge_generated_text(self,relevant_context: str,question:str, text:list[str])->str:
        #Takes as input the response the LLM sends and validates it against user's profile
        try:
          
            #raise an error if no text was provided
            if len(text) == 0:
                logger.exception("User didn't provide LLM's answer.")
                return "Please provide the generated text"

            #raise an error if prompt and text are not strings with no white spaces
            if not isinstance(question,str):
                logger.exception("User didn't provide a valid question")
                return "Question  must be valid string"

            #raise an error if the initial question wasn't provided
            if not question.strip():
                    logger.exception("User didn't provide the initial question")
                    return "Please provide user's question"
            

            if not isinstance(text, list) or not all(isinstance(t, str) for t in text):
                logger.warning("Text is not a list of strings")
                return "Text must be a list of strings"


            full_text = "".join(text)

            if not full_text.strip():
                logger.warning("LLM answer is empty")
                return "Please provide the generated text"

            #judge text
            judged_text = prompt_.validate_prompt(profile_text=relevant_context,
                            question=question,response=full_text)

            #call the llm
            response = self.chat.send_message(judged_text)
            

            print(response.text)
            return response.text
    
                       

            
          
        except errors.APIError as e:
            if e.code == 429:
                logger.exception(f"[API Rate Limit]: {e.message}")
                return  "I am currently receiving too many requests. Please try again in a moment."
            elif e.code in (400, 404):
                logger.exception(f"[API Client Error {e.code}]: {e.message}")
                return  "There was a configuration issue while processing your request."
            elif e.code in (500, 503):
                logger.exception(f"[API Server Error {e.code}]: {e.message}")
                return  "The AI service is temporarily unavailable. Please try again shortly."
            else:
                logger.exception(f"[API Error {e.code}]: {e.message}")
                return  "An unexpected service error occurred."
            
        except (httpx.ConnectError, httpx.TimeoutException, ConnectionError, TimeoutError) as e:
                logger.exception(f"Chat handler failed: {e}")
                return  "Network connection issue. Please check your internet and try again."
            
        except Exception as e:
                logger.exception(f"Chat handler failed: {e}")
                return  "An internal error occurred. Please try again."
    """


    def generate_text(self, question: str,) -> Iterator[str]:      
       
        """Yields text chunks as the model generates them."""
        try:

            #raise an error if question is not a valid string or is empty
            if not isinstance(question,str):
                logger.exception("User didn't provide a valid question")
                return "Please provide a valid question (string)"
            if not question.strip():
                logger.exception("User added an empty string with whitespaces")
                return "Question must be a valid string"
            relevant_context = chroma.retrieve_from_chroma(question)
            
            prompt = prompt_.digital_twin_prompt(
                profile_text=relevant_context,
                question=question,
            )

            #create a list to add user's fully response
            full_response = []
            message = prompt
            while True:
                function_calls = []

                for chunk in self.chat.send_message_stream(message=message):
                    if chunk.function_calls:
                        function_calls.extend(chunk.function_calls)
                    if chunk.text:
                        yield chunk.text
                        full_response.append(chunk.text)

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

            #judge message
            #self.judge_generated_text(relevant_context,question,full_response)

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

        except (httpx.ConnectError, httpx.TimeoutException, ConnectionError, TimeoutError) as e:
            logger.exception(f"Chat handler failed: {e}")
            yield  "Network connection issue. Please check your internet and try again."

        except Exception as e:
            logger.exception(f"Chat handler failed: {e}")
            yield  "An internal error occurred. Please try again."



    
   
