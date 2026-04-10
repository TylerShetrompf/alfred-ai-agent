import os
from xmlrpc import client # for accessing environment variables
from dotenv import load_dotenv # for reading environment variables from .env file
from google import genai # for interacting with Gemini API

def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content( # test call
        model = "gemini-3-flash-preview", 
        contents = "Please confirm that you have received this message. Reply in only one sentence, utilizing as few tokens as possible."
    )
    
    print(response.text)


if __name__ == "__main__":
    main()
