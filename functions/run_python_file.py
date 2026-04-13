import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    
    try:     
        
        absolute_path = os.path.abspath(working_directory)

        target_file_path = os.path.normpath(os.path.join(absolute_path, file_path))

        is_valid_target_file = os.path.commonpath([absolute_path, target_file_path]) == absolute_path

        if is_valid_target_file != True:

            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target_file_path) != True:
            
            return f'Error: "{file_path}" does not exist or is a directory'
        
        if target_file_path.endswith(".py")!= True:

            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file_path]

        if args != None:
            
            command.extend(args)

        script_output = subprocess.run(command, cwd=working_directory, capture_output=True, text=True, timeout=30)
        
        output_string = ""

        if script_output.returncode != 0:

            output_string += f'Process exited with code {script_output.returncode}\n'

        if script_output.stdout == None and script_output.stderr == None:
            
            output_string += "No output produced\n"
        
        else:

            output_string += f"STDOUT:\n\n{script_output.stdout}\n"
            output_string += f"STDERR:\n\n{script_output.stderr}"

        return output_string

    except Exception as e:

        return f"Error: {e}"
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute (run) a python file (.py file) at a specified file path relative to the working directory with specified arguments. If a user requests to run a file, use this functiosn.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path of script being executed, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Arguments to be passed with script being executed (default is None)",
            ),
        },
    ),
)