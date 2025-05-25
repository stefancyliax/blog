import pytest
from block import MarkdownParser

def test_parse_heading():
    md = "# Hello World"
    parser = MarkdownParser(md)
    assert len(parser.blocks) == 1
    assert parser.to_html() == "<div>\n<h1>Hello World</h1>\n</div>"


def test_parse_paragraph():
    md = "This is a paragraph."
    parser = MarkdownParser(md)
    assert len(parser.blocks) == 1
    assert parser.to_html() == "<div>\n<p>This is a paragraph.</p>\n</div>"


def test_parse_horizontal_rule():
    md = "---"
    parser = MarkdownParser(md)
    assert len(parser.blocks) == 1
    assert parser.to_html() == "<div>\n<hr />\n</div>"


def test_parse_code_block():
    md = "```\nimport somepackage\n```"
    parser = MarkdownParser(md)
    assert len(parser.blocks) == 1
    assert parser.to_html() == "<div>\n<pre><code>\nimport somepackage\n</code></pre>\n</div>"


def test_parse_unordered_list():
    md = "- Item 1\n- Item 2"
    parser = MarkdownParser(md)
    html = parser.to_html()
    expected = "<div>\n<ul>\n  <li>Item 1</li>\n  <li>Item 2</li>\n</ul>\n</div>"
    assert html == expected


def test_parse_ordered_list():
    md = "1. First\n2. Second"
    parser = MarkdownParser(md)
    html = parser.to_html()
    expected = "<div>\n<ol>\n  <li>First</li>\n  <li>Second</li>\n</ol>\n</div>"
    assert html == expected


def test_parse_blockquote():
    md = "> Line 1\n> Line 2"
    parser = MarkdownParser(md)
    html = parser.to_html()
    expected = "<div>\n<blockquote>\n  <p>Line 1</p>\n  <p>Line 2</p>\n</blockquote>\n</div>"
    assert html == expected


def test_parse_mixed_blocks():
    md = "# Title\n\nThis is a paragraph.\n\n- Item 1\n- Item 2"
    parser = MarkdownParser(md)
    html = parser.to_html()
    expected = (
        "<div>\n"
        "<h1>Title</h1>\n"
        "<p>This is a paragraph.</p>\n"
        "<ul>\n  <li>Item 1</li>\n  <li>Item 2</li>\n</ul>\n"
        "</div>"
    )
    assert html == expected


def test_return_blocks_count():
    md = "# Title\n\nParagraph text."
    parser = MarkdownParser(md)
    blocks = parser.return_blocks()
    assert len(blocks) == 2


#############################################

def test_long_article_like_document():
    md = """# Welcome to My Blog

This is the first paragraph of the blog post. It gives a short introduction to the topic and sets the tone.

## Why Markdown?

Markdown is a lightweight markup language that allows you to write using an easy-to-read, easy-to-write plain text format.

- It's simple to learn.
- It's widely supported.
- It converts cleanly to HTML.

## Code Example

Here is a simple Python example:


```
def greet(name):
    print(f"Hello, {name}!")
```

You can copy and paste this into your editor.

Thanks for reading!
"""
    parser = MarkdownParser(md)
    html = parser.to_html()

    expected = """<div>
<h1>Welcome to My Blog</h1>
<p>This is the first paragraph of the blog post. It gives a short introduction to the topic and sets the tone.</p>
<h2>Why Markdown?</h2>
<p>Markdown is a lightweight markup language that allows you to write using an easy-to-read, easy-to-write plain text format.</p>
<ul>
  <li>It's simple to learn.</li>
  <li>It's widely supported.</li>
  <li>It converts cleanly to HTML.</li>
</ul>
<h2>Code Example</h2>
<p>Here is a simple Python example:</p>
<pre><code>
def greet(name):
    print(f"Hello, {name}!")
</code></pre>
<p>You can copy and paste this into your editor.</p>
<p>Thanks for reading!</p>
</div>"""
    assert html == expected
    
    

def test_mixed_content_with_links_and_images():
    md = """# Project Overview

Our project aims to solve the world's most pressing issues using **cutting-edge AI**.

## Features

1. Fast and scalable
2. Open-source
3. Backed by a strong community

For more information, [visit our website](https://example.com).

![Architecture Diagram](architecture.png)

> “The best way to predict the future is to invent it.” - Alan Kay
"""
    parser = MarkdownParser(md)
    html = parser.to_html()
    expected = """<div>
<h1>Project Overview</h1>
<p>Our project aims to solve the world's most pressing issues using <strong>cutting-edge AI</strong>.</p>
<h2>Features</h2>
<ol>
  <li>Fast and scalable</li>
  <li>Open-source</li>
  <li>Backed by a strong community</li>
</ol>
<p>For more information, <a href="https://example.com">visit our website</a>.</p>
<p><img src="architecture.png" alt="Architecture Diagram" /></p>
<blockquote>
  <p>“The best way to predict the future is to invent it.” - Alan Kay</p>
</blockquote>
</div>"""
    assert html == expected



def test_codeblock_parsing():
    markdown = """## Code Example

Here is a simple Python example:

```
def greet(name):
    print(f"Hello, {name}!")
```

You can copy and paste this into your editor.

Thanks for reading!
"""

    parser = MarkdownParser(markdown)
    html = parser.to_html()
    expected_html = (
        "<div>"
        "<h2>Code Example</h2>\n"
        "<p>Here is a simple Python example:</p>\n"
        "<pre><code>def greet(name):\n    print(f\"Hello, {name}!\")\n</code></pre>\n"
        "<p>You can copy and paste this into your editor.</p>\n"
        "<p>Thanks for reading!</p>"
        "</div>"
    )

    # Remove whitespace differences
    assert html.replace(" ", "").replace("\n", "") == expected_html.replace(" ", "").replace("\n", "")