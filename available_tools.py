from google.genai import types # for handling Gemini API request and response objects

from functions.get_files_info import get_files_info, schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_file_contents
from functions.run_python_file import run_python_file, schema_run_python_file
from functions.write_file import write_file, schema_write_file


# create tool object with functions available to agent
available_tools = types.Tool(
    function_declarations=[schema_get_files_info,schema_get_file_contents,schema_run_python_file,schema_write_file]
)
