import os
import pytest
from block import MarkdownParser
from helper import read_file  


@pytest.mark.parametrize("md_filename, html_filename", [
    ("markdown_example1.md", "markdown_example1_expected.html"), 
    ("markdown_example2.md", "markdown_example2_expected.html"),
    #("example2.md", "example2_expected.html"),
    # Add more test files here
])

def test_markdown_to_html(md_filename, html_filename):
    base_dir = os.path.dirname(__file__)
    md_path = os.path.join(base_dir, md_filename)
    html_path = os.path.join(base_dir, html_filename)

    # Read and parse markdown
    markdown = read_file(md_path)
    parser = MarkdownParser(markdown)
    result_html = parser.to_html().strip()

    # Read expected output
    expected_html = read_file(html_path)

    assert result_html == expected_html
