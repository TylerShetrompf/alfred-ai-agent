import os
import subprocess

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