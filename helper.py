import os
import shutil


DEBUG = True

def copy_folder_contents(source_folder, target_folder):
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
    List all files in a directory matching a specific pattern.
    
    :param directory: Directory to search in.
    :param pattern: Pattern to match files against.
    :return: List of matching file paths.
    """
    import fnmatch

    matches = []
    for root, dirs, files in os.walk(directory):
        for filename in fnmatch.filter(files, pattern):
            matches.append(os.path.join(root, filename))
    return matches

def read_markdown_file(file_path):
    """
    Read the content of a markdown file.
    
    :param file_path: Path to the markdown file.
    :return: Content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def debug_print(msg):
    if DEBUG:
        print(msg)

def starts_with_number_dot(s):
    if s == "" or not s[0].isdigit():
        return False
    parts = s[:4].split('.', 1)
    return len(parts) > 1 and parts[0].isdigit()
