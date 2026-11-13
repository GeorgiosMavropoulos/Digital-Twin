import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
from google.genai import errors
from backend.tools.tool import Tools
from backend.vector_db.vec_db import ChromaDb
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

    def generate_text(self, question: str,) -> str:
        """Generates text from a prompt using the initialized client."""     
        
       
        try:
            # 1. Retrieve relevant context based on the user's question
            relevant_context = chroma.retrieve_from_chroma(question)

            #build the prompt
            prompt = prompt_.digital_twin_prompt(
                profile_text=relevant_context,
                question=question
            )
            
            response = self.chat.send_message(message=prompt)

            #create a loop to if llm called a tool
            while response.function_calls:
                tool_responses = []
                for call in response.function_calls:
                    result =tool.execute(call.name, call.args)
                    tool_responses.append(
                        types.Part.from_function_response(
                            name=call.name,
                            response={"result": result},
                        )
                    )
                response = self.chat.send_message(tool_responses)
            
            # validate if response is empty
            if not response.text:
                return "I apologize, I could not generate a response for that request."
                
            return response.text

        except errors.APIError as e:
            if e.code == 429:
                print(f"[API Rate Limit]: {e.message}")
                return "I am currently receiving too many requests. Please try again in a moment."
            elif e.code in (400, 404):
                print(f"[API Client Error {e.code}]: {e.message}")
                return "There was a configuration issue while processing your request."
            elif e.code in (500, 503):
                print(f"[API Server Error {e.code}]: {e.message}")
                return "The AI service is temporarily unavailable. Please try again shortly."
            else:
                print(f"[API Error {e.code}]: {e.message}")
                return "An unexpected service error occurred."

        except (ConnectionError, TimeoutError) as e:
            print(f"[Network Error]: {e}")
            return "Network connection issue. Please check your internet and try again."

        except Exception as e:
            print(f"[Unexpected Error]: {e}")
            return "An internal error occurred. Please try again."



    
   
