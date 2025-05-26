import pytest
from text import (
    TextNode, BoldNode, ItalicNode, CodeNode,
    LinkNode, ImageNode, ListItemNode
)

# --- TextNode --^
def test_text_node():
    node = TextNode("plain text")
    assert node.to_html() == "plain text"
    assert repr(node) == "TextNode(plain text)"

# --- BoldNode ---
def test_bold_node():
    node = BoldNode("**bold**")
    assert node.to_html() == "<b>bold</b>"
    assert repr(node) == "BoldNode(bold)"

# --- ItalicNode ---
def test_italic_node():
    node = ItalicNode("_italic_")
    assert node.to_html() == "<i>italic</i>"
    assert repr(node) == "ItalicNode(italic)"

# --- CodeNode ---
def test_code_node():
    node = CodeNode("`code`")
    assert node.to_html() == "<code>code</code>"
    assert repr(node) == "CodeNode(code)"

# --- LinkNode ---
def test_link_node():
    node = LinkNode("[OpenAI](https://openai.com)")
    assert node.to_html() == '<a href="https://openai.com">OpenAI</a>'
    assert node.text == "OpenAI"
    assert node.url == "https://openai.com"
    assert repr(node) == "LinkNode(OpenAI - https://openai.com)"

def test_link_node_invalid():
    with pytest.raises(Exception, match="Invalid link format"):
        LinkNode("not a [link]")

# --- ImageNode ---
def test_image_node():
    node = ImageNode("![dog](dog.jpg)")
    assert node.to_html() == '<img src="dog.jpg" alt="dog" />'
    assert node.text == "dog"
    assert node.url == "dog.jpg"
    assert repr(node) == "ImageNode(dog - dog.jpg)"

def test_image_node_invalid():
    with pytest.raises(Exception, match="Invalid image format"):
        ImageNode("not an image")

# --- ListItemNode ---
def test_list_item_node_html_empty():
    node = ListItemNode()
    assert node.to_html() == ""
    assert repr(node) == "ListItemNode()"
