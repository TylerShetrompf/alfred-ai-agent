from google.genai import types # for handling Gemini API request and response objects

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_contents
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file

from constants import WORKING_DIR

# create tool object with functions available to agent
available_tools = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_contents,schema_run_python_file,schema_write_file]
)


# function to call functions
def call_function(function_call, verbose=False):
    
    # handle verbose arg
    if verbose != False:
        
        print(f"Calling function: {function_call.name}({function_call.args})")

    else:
        print(f" - Calling function: {function_call.name}")

    # map function names to actual functions in dictionary
    function_map = {
        "get_file_content": get_file_content,
        "get_files_info": get_files_info,
        "run_python_file": run_python_file,
        "write_file": write_file
    }

    # make sure function name exists else it is blank
    func_name = function_call.name or ""

    # return error if function name does not exist
    if func_name not in function_map:
        
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=func_name,
                    response={"error": f"Unknown function: {func_name}"},
                )
            ],
        )
    
    else:
        # add arguments to copy dictionary if they exist, otherwise blank dict
        args = dict(function_call.args) if function_call.args else {}
        
        # manually set working directory for testing
        args["working_directory"] = WORKING_DIR

        # execute function and store result
        function_result = function_map[func_name](**args)

    # Return results as Content object
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=func_name,
                response={"result": function_result},
            )
        ],
    )