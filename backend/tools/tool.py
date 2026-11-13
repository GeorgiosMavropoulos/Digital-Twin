"""This class contains tools the LLM can use."""
from google.genai import types
class Tools:
    def __init__(self):

        #save emails schema
        self.save_emails_schema = types.Tool(
            function_declarations=[
                types.FunctionDeclaration(
                    name="collect_emails",
                    description="Saves one or more visitor email addresses to emails.txt.",
                    parameters=types.Schema(
                        type=types.Type.OBJECT,
                        properties={
                            "email": types.Schema(
                                type=types.Type.ARRAY,
                                items=types.Schema(type=types.Type.STRING),
                                description="List of email addresses provided by the visitor.",
                            ),
                        },
                        required=["email"],
                    ),
                ),
                
            ]
        )

    def execute(self, function_name: str, args: dict) -> str:
        """Dynamicaly execute tool calls."""
        method = getattr(self, function_name, None)

        if not callable(method):
            return f"Error: Tool '{function_name}' does not exist."

        return method(**args)

    def collect_emails(self,email:str)->str:
        """Collects an email address and saves it to a local text file for further examination.

            Args:
                email: The email address to save.
            """       

        #write in txt
        if not email:
            return "Error: No email addresses were provided."

        try:
            with open("emails.txt", "a", encoding="utf-8") as file:
                for email in email:
                    file.write(f"{email}\n")
            return f"Success: Saved {', '.join(email)} to emails.txt."

        except OSError as e:
            return f"Error: Could not write to file ({e})."