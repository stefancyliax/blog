from block import *
import os
from helper import copy_folder_contents, list_files_in_directory, LOG_LEVEL_INFO, debug_print, set_log_level_from_string
import sys
import argparse

def main():
    parser = argparse.ArgumentParser(description="Static site generator for a blog.")
    parser.add_argument(
        "basepath",
        nargs="?",
        default="/",
        help="The base path for URLs in the generated site (e.g., '/blog/'). Defaults to '/'."
    )
    parser.add_argument(
        "--log-level",
        "-l",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set the logging level. Defaults to INFO."
    )
    args = parser.parse_args()

    basepath = args.basepath
    # Set the global log level based on the command-line argument
    set_log_level_from_string(args.log_level)

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
    debug_print(f"Found {len(article_list)} articles.", LOG_LEVEL_INFO)
    for article in article_list:
        print(f"Processing article: {article}")
        content = read_file(article)
        doc = MarkdownParser(content)
        folder_name = os.path.basename(article).replace('.md', '')
        os.makedirs(f"docs/blog/{folder_name}", exist_ok=True)
        doc.generate_page("static/template.html", f"docs/blog/{folder_name}/index.html", basepath)

    # TODO: automatic listing and parsing of all files in content/blog/ and other
    # TODO: strip out boot.dev stuff
    # TODO: automatic detection of test cases in test_parsefile.py
    

    # t = TextParser(md3)
    # print("Parsed Markdown:")
    # t.parse_text()
    


if __name__ == "__main__":
    main()
