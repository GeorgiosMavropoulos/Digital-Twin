import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()
class LLMService:
    def __init__(self,  default_model: str = "gemini-3.5-flash-lite", system_instruction: str | None = None):
        """
        Initialize the Gemini client. 
        Falls back to the GEMINI_API_KEY environment variable if api_key is not passed.
        """
        self.default_model = default_model
        self.client = genai.Client()

        config = None
        if system_instruction:
            config = types.GenerateContentConfig(system_instruction=system_instruction)

        # Initialize the chat ONCE so history persists across generate_text() calls
        self.chat = self.client.chats.create(
            model=self.default_model,
            config=config
        )

    def generate_text(self, prompt: str,system_instruction: str | None = None) -> str:
        """Generates text from a prompt using the initialized client."""
        
        
        config = None
        if system_instruction:
            config = types.GenerateContentConfig(system_instruction=system_instruction)

       
        response = self.chat.send_message(
            
            message=prompt,
            config=config
        )
      
        return response.text


if __name__ == "__main__":
    
    gemini = LLMService()
    print('Press bye to leave')

    user_input = ''
    while user_input != 'bye':
        user_input = str(input('I am available, hello there: ')).lower()
        prompt = gemini.generate_text(user_input,'You are a helpful assistant.')

         # Skip empty presses
        if not user_input:
            continue
        print(prompt)
    
   
