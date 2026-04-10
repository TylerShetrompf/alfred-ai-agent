import os
from dotenv import load_dotenv # for reading environment variables from .env file
from google import genai # for interacting with Gemini API
import argparse # for parsing arguments passed via cli
from google.genai import types 

# function to call api with content
def call_model(client, messages):
    
    # send prompt and return response
    response = client.models.generate_content( 
        model = "gemini-3-flash-preview", 
        contents = messages
    )

    return response

# function to check for response metadata, then print token info and return text. otherwise raise error
def check_metadata(response):
    
    if response.usage_metadata != None:
        
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        
        return response.text
    
    else:
        
        raise RuntimeError("No usage_metadata received, API request failure likely.")


def get_api_key():
    
    #loads .env file and gets api key
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    # raise an error if api_key not found
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY environment variable not set.")

    return api_key

def main():

    # Parse prompt given via cli
    prompt_parser = argparse.ArgumentParser(description="Alfred")
    prompt_parser.add_argument("user_prompt", type = str, help = "Prompt for Alfred")
    args = prompt_parser.parse_args()

    # call func to retrieve api key
    api_key = get_api_key()

    # create client object with api_key
    client = genai.Client(api_key=api_key)

    # set users prompt as message
    messages = [types.Content(role="user", parts=[types.Part(text = args.user_prompt)])]

    # call model and store entire response
    response = call_model(client, messages)
    
    # send response to metadata check function
    response_text = check_metadata(response)

    # print response to CLI
    print(response_text)

    

if __name__ == "__main__":
    main()
