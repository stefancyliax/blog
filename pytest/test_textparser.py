import pytest
from text import TextParser, TextNode, BoldNode, ItalicNode, CodeNode, LinkNode, ImageNode, ListItemNode

def test_extract_bold():
    parser = TextParser("")
    result = parser.extract_bold("This is **bold** text")
    assert result == [(8, "**bold**")]

def test_extract_italic():
    parser = TextParser("")
    result = parser.extract_italic("This is _italic_ text")
    assert result == [(8, "_italic_")]

def test_extract_inline_code():
    parser = TextParser("")
    result = parser.extract_inline_code("Some `code` here")
    assert result == [(5, "`code`")]

def test_extract_links():
    parser = TextParser("")
    result = parser.extract_links("Visit [Google](https://google.com)")
    assert result == [(6, "[Google](https://google.com)")]

def test_extract_images():
    parser = TextParser("")
    result = parser.extract_images("Here is an image ![alt](image.jpg)")
    assert result == [(17, "![alt](image.jpg)")]

def test_parse_text_nodes():
    parser = TextParser("Hello **bold** world")
    nodes = parser.parse_text()
    assert isinstance(nodes[0], TextNode)
    assert nodes[0].text == "Hello "
    assert isinstance(nodes[1], BoldNode)
    assert nodes[1].text == "bold"
    assert isinstance(nodes[2], TextNode)
    assert nodes[2].text == " world"

def test_parse_text_with_all_features():
    parser = TextParser("This is _italic_, **bold**, and `code` plus a [link](http://x.com) and ![img](y.png)")
    nodes = parser.parse_text()
    assert any(isinstance(n, ItalicNode) for n in nodes)
    assert any(isinstance(n, BoldNode) for n in nodes)
    assert any(isinstance(n, CodeNode) for n in nodes)
    assert any(isinstance(n, LinkNode) for n in nodes)
    assert any(isinstance(n, ImageNode) for n in nodes)

def test_parse_list_items():
    markdown = "- Item one\n* Item two\n1. Item three\nPlain text"
    parser = TextParser(markdown)
    nodes = parser.parse_text_and_list()

    list_items = [n for n in nodes if isinstance(n, ListItemNode)]
    assert len(list_items) == 3

    texts = [n.text for n in nodes if isinstance(n, TextNode)]
    assert "Item one" in texts
    assert "Item two" in texts
    assert "Item three" in texts
    assert "Plain text" in texts

def test_extract_markdown_images():
    parser = TextParser("")
    result = parser.extract_markdown_images("Text ![dog](dog.jpg) and ![cat](cat.png)")
    assert result == [(5, "![dog](dog.jpg)"), (25, "![cat](cat.png)")]

def test_extract_newlines():
    parser = TextParser("")
    result = parser.extract_newlines("This is a text\nwith some newlines\nand more")
    assert result == [(14, "\n"), (33, "\n")]
