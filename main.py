from block import MarkdownParser, debug_print, read_file
import os
from helper import copy_folder_contents, list_files_in_directory
import sys

# Define constants
CONTENT_DIR = "content"
STATIC_DIR = "static"
OUTPUT_DIR = "docs"
TEMPLATE_NAME = "template.html"

def generate_html_page(markdown_source_path, output_html_path, template_full_path, current_basepath):
    """
    Reads markdown content, parses it, and generates an HTML page.
    """
    print(f"Generating page from {markdown_source_path} to {output_html_path} using template {template_full_path}")
    md_content = read_file(markdown_source_path)
    doc = MarkdownParser(md_content)
    os.makedirs(os.path.dirname(output_html_path), exist_ok=True)
    doc.generate_page(template_full_path, output_html_path, current_basepath)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    print(f"Hello from blog! Generating site with basepath: '{basepath}'")

    # Calculate paths based on constants and basepath
    static_root_output_dir = os.path.join(OUTPUT_DIR, basepath.strip("/"), "")
    template_full_path = os.path.abspath(os.path.join(STATIC_DIR, TEMPLATE_NAME))
    html_output_root = os.path.join(OUTPUT_DIR, basepath.strip("/"), "")

    # Copy static files
    copy_folder_contents(STATIC_DIR, static_root_output_dir)
    print(f"Static files copied to: {static_root_output_dir}")

    # Generate index page
    print("\nProcessing index page...")
    index_md_src = os.path.join(CONTENT_DIR, "index.md")
    index_html_dest = os.path.join(html_output_root, "index.html")
    generate_html_page(index_md_src, index_html_dest, template_full_path, basepath)
    
    # Generate contact page
    print("\nProcessing contact page...")
    contact_md_src = os.path.join(CONTENT_DIR, "contact", "contact.md")
    contact_html_dest = os.path.join(html_output_root, "contact", "index.html")
    generate_html_page(contact_md_src, contact_html_dest, template_full_path, basepath)

    # Generate articles
    print("\nProcessing articles...")
    articles_content_dir = os.path.join(CONTENT_DIR, "articles")
    article_files = list_files_in_directory(articles_content_dir, "*.md")
    debug_print(f"Found {len(article_files)} articles.")

    for article_markdown_path in article_files:
        print(f"Processing article: {article_markdown_path}")
        folder_name = os.path.basename(article_markdown_path).replace('.md', '')
        article_html_dest = os.path.join(html_output_root, "blog", folder_name, "index.html")
        generate_html_page(article_markdown_path, article_html_dest, template_full_path, basepath)

    print("\n###################################")
    print("Site generation complete.")
    #TODO: referencing the .css in the subfolders is not working (This might be resolved by correct basepath handling now)

if __name__ == "__main__":
    main()
