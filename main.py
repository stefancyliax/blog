from block import *
import os
from helper import copy_folder_contents, list_files_in_directory

def main():
    print("Hello from blog!")

    md = "# Hello World\n\nThis is a **simple** paragraph.\nand another line\n\nAnother paragraph.\n\n## Subheading\n\nand some more text"

    md2 = """
Here is an image: ![dog](dog.jpg)
Another one ![cat](cat.png) in the same paragraph.

> lorem ipsum dolor **sit amet**, consectetur adipiscing elit.
> **sed do eiusmod** tempor incididunt ut labore et dolore magna aliqua.
> ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
> and more

sone some more text here.
"""

    md3 = "This _is_ a single **paragrpah** thi ![dog](dog.jpg) with some **bold text** and _some italic text_ and `some code` too."

    # doc = MarkdownParser(md2)
    # print("Parsed Markdown:")
    # print(doc.return_blocks())

    # print("\n\n")
    # print(doc.to_html())

    copy_folder_contents("static/","docs/")

    md_content = read_file("content/index.md")
    doc = MarkdownParser(md_content)
    doc.generate_page("static/template.html","docs/index.html")
    print("###################################")
    
    md_contact = read_file("content/contact/contact.md")
    doc = MarkdownParser(md_contact)
    os.makedirs(f"docs/contact", exist_ok=True)
    doc.generate_page("static/template.html", "docs/contact/index.html")

    article_list = list_files_in_directory("content/articles", "*.md")
    debug_print(f"Found {len(article_list)} articles.")
    for article in article_list:
        print(f"Processing article: {article}")
        content = read_file(article)
        doc = MarkdownParser(content)
        folder_name = os.path.basename(article).replace('.md', '')
        os.makedirs(f"docs/blog/{folder_name}", exist_ok=True)
        doc.generate_page("static/template.html", f"docs/blog/{folder_name}/index.html")

    #TODO: referencing the .css in the subfolders is not working

    # t = TextParser(md3)
    # print("Parsed Markdown:")
    # t.parse_text()
    


if __name__ == "__main__":
    main()
