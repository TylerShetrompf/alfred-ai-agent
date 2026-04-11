import os
from constants import MAX_READ_CHARS

def get_file_content(working_directory, file_path):
    
    try:
        
        absolute_path = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(absolute_path, file_path))

        is_valid_target_file = os.path.commonpath([absolute_path, target_file]) == absolute_path

        if is_valid_target_file != True:
        
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isfile(target_file) != True:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as file:
            contents = file.read(MAX_READ_CHARS)
            # After reading the first MAX_CHARS...
            if file.read(1):
                contents += f'[...File "{file_path}" truncated at {MAX_READ_CHARS} characters]'
            return contents
    
    except Exception as e:
        return f"Error: {e}"