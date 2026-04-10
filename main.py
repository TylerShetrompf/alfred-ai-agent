import os
from xmlrpc import client # for accessing environment variables
from dotenv import load_dotenv # for reading environment variables from .env file
from google import genai # for interacting with Gemini API
import argparse # for parsing arguments passed via cli

def main():

    # Parse prompt given via cli
    prompt_parser = argparse.ArgumentParser(description="Alfred")
    prompt_parser.add_argument("user_prompt", type = str, help = "Prompt for Alfred")
    args = prompt_parser.parse_args()

    #loads .env file and gets api key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # raise an error if api_key not found
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    # create client object with api_key
    client = genai.Client(api_key=api_key)

    # send prompt and store response
    response = client.models.generate_content( 
        model = "gemini-3-flash-preview", 
        contents = args.user_prompt
    )

    # check for response metadata, then print info. otherwise raise error
    if response.usage_metadata != None:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        print(response.text)
    else:
        raise RuntimeError("No usage_metadata received, API request failure likely.")


if __name__ == "__main__":
    main()
