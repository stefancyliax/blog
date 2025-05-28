import os
import shutil


DEBUG = False


def copy_folder_contents(source_folder, target_folder):
    """
    Copies the contents of a source folder to a target folder.

    The target folder is cleaned up before copying. If the target folder
    doesn't exist, it will be created.

    Args:
        source_folder (str): The path to the source folder.
        target_folder (str): The path to the target folder.
    """
    # Ensure both paths are absolute
    source_folder = os.path.abspath(source_folder)
    target_folder = os.path.abspath(target_folder)

    # Clean up the target folder
    if os.path.exists(target_folder):
        for filename in os.listdir(target_folder):
            file_path = os.path.join(target_folder, filename)
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
    else:
        os.makedirs(target_folder)

    # Recursively copy files and directories from source to target
    for root, dirs, files in os.walk(source_folder):
        # Compute the relative path from source_folder
        rel_path = os.path.relpath(root, source_folder)
        dest_dir = os.path.join(target_folder, rel_path)
        os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dst_file = os.path.join(dest_dir, file)
            shutil.copy2(src_file, dst_file)

def list_files_in_directory(directory, pattern):
    """
    Lists all files in a directory that match a specific pattern.
    
    Args:
        directory (str): The directory to search in.
        pattern (str): The pattern to match files against (e.g., "*.txt").
    
    Returns:
        list: A list of file paths for the matching files.
    """
    import fnmatch

    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def read_file(file_path):
    """
    Reads the content of a file.
    
    Args:
        file_path (str): The path to the file.
        
    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def debug_print(msg):
    """
    Prints a message to the console if the DEBUG flag is True.

    Args:
        msg (str): The message to print.
    """
    if DEBUG:
        print(msg)

def starts_with_number_dot(s):
    """
    Checks if a string starts with a number followed by a dot.

    This is used to identify ordered list items (e.g., "1.", "2.").
    It checks up to the first 4 characters of the string.

    Args:
        s (str): The string to check.

    Returns:
        bool: True if the string starts with a number followed by a dot, False otherwise.
    """
    if s == "" or not s[0].isdigit():
        return False
    parts = s[:4].split('.', 1)
    return len(parts) > 1 and parts[0].isdigit()
