import pytest
from block import (
    HeadingBlock,
    ParagraphBlock,
    RuleBlock,
    CodeBlock,
    UnorderedListBlock,
    OrderedListBlock,
    BlockQuoteBlock,
)


def test_heading_block():
    heading = HeadingBlock("### This is a heading")
    assert heading.to_html() == "<h3>This is a heading</h3>"
    assert heading.heading_level == 3
    assert heading.title == "This is a heading"


def test_paragraph_block():
    paragraph = ParagraphBlock("This is a simple paragraph.")
    assert paragraph.to_html() == "<p>This is a simple paragraph.</p>"


def test_rule_block():
    rule = RuleBlock()
    assert rule.to_html() == "<hr />"


def test_unordered_list_block():
    block = "- Item one\n- Item two"
    ul_block = UnorderedListBlock(block)
    expected = "<ul>\n  <li>Item one</li>\n  <li>Item two</li>\n</ul>"
    assert ul_block.to_html() == expected


def test_ordered_list_block():
    block = "1. First item\n2. Second item"
    ol_block = OrderedListBlock(block)
    expected = "<ol>\n  <li>First item</li>\n  <li>Second item</li>\n</ol>"
    assert ol_block.to_html() == expected


def test_blockquote_block():
    block = "> Quoted line 1\n> Quoted line 2"
    quote_block = BlockQuoteBlock(block)
    expected = "<blockquote>\n  <p>Quoted line 1</p>\n  <p>Quoted line 2</p>\n</blockquote>"
    assert quote_block.to_html() == expected


def test_blockquote_block2():
    block = """
> "I am in fact a Hobbit in all but size."
> 
> -- J.R.R. Tolkien
"""
    quote_block = BlockQuoteBlock(block)
    expected = '''<blockquote>
  <p>"I am in fact a Hobbit in all but size."</p>
  <p></p>
  <p>-- J.R.R. Tolkien</p>
</blockquote>'''
    assert quote_block.to_html() == expected



def test_code_block():
    block = """
```
print('Hello')
```
"""
    code_block = CodeBlock(block)    
    excepted = "<pre><code>\nprint('Hello')\n</code></pre>"
    assert code_block.to_html() == excepted




def test_code_block2():
    block = """
```
def greet(name):
    print(f"Hello, {name}!")

```
"""
    code_block = CodeBlock(block)    
    excepted = '<pre><code>\ndef greet(name):\n    print(f"Hello, {name}!")\n\n</code></pre>'
    assert code_block.to_html() == excepted


