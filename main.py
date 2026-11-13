"""Main entry point to interact with the LLM"""
from backend.llm.llm_client import LLMService
from backend.prompts.prompt_templates import PromptTemplates
from backend.vector_db.vec_db import ChromaDb
chroma = ChromaDb()
prompt_ = PromptTemplates()
llm_client = LLMService()

def main():
    """Main entry"""

    #store the pdf so the model can answer
    chroma.store_pdf_in_chroma("Profile.pdf")

    while True:
      
        #question
        question = input('Insert your question or type bye: ').lower()
        if question == 'bye':
            break
        relevant_context = chroma.retrieve_from_chroma(question)
        #prompt
        prompt = prompt_.digital_twin_prompt(profile_text=relevant_context,question=question)
        
        answer = llm_client.generate_text(prompt)
        print(answer)

main()

    