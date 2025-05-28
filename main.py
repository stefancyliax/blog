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

    # Scan for all markdown files in the content directory
    all_md_files = list_files_in_directory("content/", "*.md")
    # Exclude content/index.md from this list as it's handled separately
    all_md_files = [f for f in all_md_files if os.path.normpath(f) != os.path.normpath("content/index.md")]
    debug_print(f"Found {len(all_md_files)} other markdown files: {all_md_files}")

    generated_pages_links = [] # To store info for linking later

    # Process all markdown files found (excluding index.md)
    for md_file_path in all_md_files:
        print(f"Processing file: {md_file_path}")
        content = read_file(md_file_path)
        doc = MarkdownParser(content)

        # Determine the output path, preserving the directory structure from 'content'
        relative_path = os.path.relpath(md_file_path, "content/")
        link_title = doc.blocks[0].title if doc.blocks and hasattr(doc.blocks[0], 'title') and doc.blocks[0].title else os.path.splitext(os.path.basename(md_file_path))[0]
        link_url_suffix = ""
        # For 'contact/contact.md' -> 'contact/index.html'
        # For 'articles/my-article.md' -> 'blog/my-article/index.html'
        if relative_path.startswith("articles" + os.sep):
            folder_name = os.path.splitext(os.path.basename(md_file_path))[0]
            dest_folder = os.path.join("docs/blog", folder_name)
            dest_file_name = "index.html"
            link_url_suffix = f"blog/{folder_name}/"
        else: # Handles contact/contact.md and any other direct .md files in subdirectories
            dest_folder = os.path.join("docs", os.path.dirname(relative_path))
            if os.path.splitext(os.path.basename(md_file_path))[0] == os.path.basename(os.path.dirname(md_file_path)):
                 dest_file_name = "index.html"
                 link_url_suffix = f"{os.path.dirname(relative_path)}/"
            else:
                file_name_without_ext = os.path.splitext(os.path.basename(md_file_path))[0]
                dest_folder = os.path.join(dest_folder, file_name_without_ext)
                dest_file_name = "index.html"
                link_url_suffix = f"{os.path.dirname(relative_path)}/{file_name_without_ext}/"
                if os.path.dirname(relative_path) == ".": # if the file is in the root of content (e.g. content/about.md)
                    link_url_suffix = f"{file_name_without_ext}/"


        os.makedirs(dest_folder, exist_ok=True)
        dest_path = os.path.join(dest_folder, dest_file_name)
        
        doc.generate_page("static/template.html", dest_path, basepath)
        print(f"Generated page for {md_file_path} at {dest_path}")
        generated_pages_links.append({"title": link_title, "url": basepath + link_url_suffix})

    # After all pages are generated, update docs/index.html with links
    if generated_pages_links:
        index_html_path = "docs/index.html"
        index_content = read_file(index_html_path)
        
        links_html = "<h2>Other Pages</h2>\n<ul>\n"
        for link_info in generated_pages_links:
            links_html += f'  <li><a href="{link_info["url"]}">{link_info["title"]}</a></li>\n'
        links_html += "</ul>\n"
        
        # Try to insert before the last </body> tag, or a common footer.
        # A more robust way would be a placeholder in template.html like {{ Other_Pages_Links }}
        if "</body>" in index_content:
            index_content = index_content.replace("</body>", f"{links_html}</body>", 1)
        elif "</div>" in index_content: # Fallback: insert before the last closing div
             # Find the last occurrence of </div>
            last_div_pos = index_content.rfind("</div>")
            if last_div_pos != -1:
                index_content = index_content[:last_div_pos] + links_html + index_content[last_div_pos:]
            else: # If no </body> or </div>, just append
                index_content += links_html
        else: # Fallback, just append
            index_content += links_html

        with open(index_html_path, "w", encoding='utf-8') as f:
            f.write(index_content)
        print(f"Updated {index_html_path} with links to other pages.")

    #TODO: referencing the .css in the subfolders is not working

    # t = TextParser(md3)
    # print("Parsed Markdown:")
    # t.parse_text()
    


if __name__ == "__main__":
    main()
