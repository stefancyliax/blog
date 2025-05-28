from block import *
import os
from helper import copy_folder_contents, list_files_in_directory
import sys

def main():
    """
    Main function for the static site generator.

    This function performs the following steps:
    1. Sets the basepath for URLs (defaults to "/" or can be provided as a command-line argument).
    2. Copies the contents of the "static/" folder to "docs/".
    3. Parses "content/index.md", generates an HTML page using "static/template.html", and saves it to "docs/index.html".
    4. Parses "content/contact/contact.md", generates an HTML page, and saves it to "docs/contact/index.html".
    5. Finds all markdown files in "content/articles/", parses each, generates an HTML page, and saves them to "docs/blog/<article_name>/index.html".
    """
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    print("Hello from blog!")

    copy_folder_contents("static/","docs/")

    md_content = read_file("content/index.md")
    doc = MarkdownParser(md_content)
    doc.generate_page("static/template.html","docs/index.html", basepath)
    print("###################################")
    
    md_contact = read_file("content/contact/contact.md")
    doc = MarkdownParser(md_contact)
    os.makedirs(f"docs/contact", exist_ok=True)
    doc.generate_page("static/template.html", "docs/contact/index.html", basepath)

    article_list = list_files_in_directory("content/articles", "*.md")
    debug_print(f"Found {len(article_list)} articles.")
    for article in article_list:
        print(f"Processing article: {article}")
        content = read_file(article)
        doc = MarkdownParser(content)
        folder_name = os.path.basename(article).replace('.md', '')
        os.makedirs(f"docs/blog/{folder_name}", exist_ok=True)
        doc.generate_page("static/template.html", f"docs/blog/{folder_name}/index.html", basepath)

    #TODO: referencing the .css in the subfolders is not working

    # t = TextParser(md3)
    # print("Parsed Markdown:")
    # t.parse_text()
    


if __name__ == "__main__":
    main()
