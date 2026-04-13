import os
import time
import sys

from dotenv import load_dotenv # for reading environment variables from .env file

from google import genai # for interacting with Gemini API
from google.genai import types # for handling Gemini API request and response objects

import argparse # for parsing arguments passed via cli

from prompts import system_prompt # imports the system prompt

from available_tools import available_tools, call_function

# function to call api with content
def call_model(client, messages):
    
    # updated to use try/except due to constant 503 errors
    attempt = 0
    max_retries = 30
    delay = 5

    while attempt < max_retries:
        
        try:
            # send prompt and return response
            response = client.models.generate_content( 
                model = "gemini-2.5-flash", 
                contents = messages,
                config = types.GenerateContentConfig(tools=[available_tools], system_instruction=system_prompt)
            )
            return response

        
        except Exception as e:
            attempt += 1
            print(f"Attempt {attempt} failed: {e}")

            if attempt < max_retries:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
            else:
                print("All retries failed.")
                raise  # Re-raise the last exception



# function to check for response metadata and return text or raise error if none
def check_metadata(response):
    
    if response.usage_metadata != None:
        
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

# func to parse args via cli
def parse_args():
    
    # ArgumentParser object
    prompt_parser = argparse.ArgumentParser(description="Alfred")
    
    # add args to parse for
    prompt_parser.add_argument("user_prompt", type = str, help = "Prompt for Alfred")
    prompt_parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    
    # store and return args
    args = prompt_parser.parse_args()
    return args       

def main():

    # call func to get args:
    args = parse_args()

    # call func to retrieve api key
    api_key = get_api_key()

    # create client object with api_key
    client = genai.Client(api_key=api_key)

    # set users prompt as message
    messages = [types.Content(role="user", parts=[types.Part(text = args.user_prompt)])]

    response_text = ""

    for _ in range(20):

        # call model and store entire response
        response = call_model(client, messages)
        
        # check candidates 
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)

        # send response to metadata check function (returns response text)
        response_text = check_metadata(response)

        # handle verbose argument
        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # init empty list for function results
        function_results = []

        if response.function_calls != None:
            for call in response.function_calls:
                function_call_result = call_function(call)

                # Handle missing response
                if not function_call_result.parts:
                    raise Exception("Error: Call function response parts empty.")
                elif function_call_result.parts[0].function_response == None or function_call_result.parts[0].function_response.response == None:
                    raise Exception("Error: Function call response is empty.")
                
                else:
                    # store result of function call
                    function_results.append(function_call_result.parts[0])
                    
                    # handle verbose argument
                    if args.verbose == True: 
                        print(f"-> {function_call_result.parts[0].function_response.response}")
            
            # append function results to messages
            messages.append(types.Content(role="user", parts=function_results))
        
        #if no function calls, check that there is response text:
        elif response_text == None:
            print("Error: No response received.")
            sys.exit(1)
        else:
            print(response_text)
            break

                
    

if __name__ == "__main__":
    main()
