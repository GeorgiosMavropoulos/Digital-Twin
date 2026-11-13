"""This class contains tools the LLM can use."""

class Tools:
    def __init__(self):
        pass


    def collect_emails(email:str):
        """Collects an email address and saves it to a local text file for further examination.

            Args:
                email: The email address to save.
            """

        #write in txt
        try:
            with open("emails.txt", "a", encoding="utf-8") as file:
                file.write(email)

        except FileNotFoundError:
            print("Error: The directory or folder path does not exist.")

        except PermissionError:
            print("Error: You do not have permission to write to this file.")

        except OSError as e:
            print(f"A system error occurred: {e}")

        else:
            print("File written successfully!")