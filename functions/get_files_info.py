import os

def get_files_info(working_directory, directory="."):
    
    try:

        absolute_path = os.path.abspath(working_directory)
        target_directory = os.path.normpath(os.path.join(absolute_path, directory))

        is_valid_target_dir = os.path.commonpath([absolute_path, target_directory]) == absolute_path

        # Make sure path is valid directory
        if os.path.isdir(target_directory) != True:
            return f'Error: "{target_directory}" is not a directory'
        
        # Make sure path is in permitted directory
        if is_valid_target_dir != True:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        # Get list of items in dir
        items_in_dir = os.listdir(target_directory)

        string = ""

        # Put together and return output string
        for item in items_in_dir:
            item_path = os.path.join(target_directory, item)
            if os.path.isdir(item_path) == True:
                string += f"- {item}: file_size={os.path.getsize(item_path)}, is_dir=True"
            else:
                string += f"- {item}: file_size={os.path.getsize(item_path)}, is_dir=False"
            string += "\n"
        return string
    
    # Handle exceptions
    except Exception as e:
        return f"Error: {e}"