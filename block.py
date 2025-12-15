from helper import debug_print, starts_with_number_dot, read_file
from text import *
import os
       

class MarkdownParser():
    """
    Parses markdown text into a list of block objects.
    """
    def __init__(self, markdown):
        """
        Initializes the MarkdownParser object.

        Args:
            markdown (str): The markdown text to parse.
        """
        self.n_blocks = 0
        self.blocks = []
        self.parse_markdown(self.split_blocks(markdown))

    def add_block(self, block):
        """
        Adds a block to the list of blocks.

        Args:
            block: The block object to add.
        """
        self.blocks.append(block)
        self.n_blocks += 1

    def return_blocks(self):
        """
        Returns the list of block objects.

        Returns:
            list: The list of block objects.
        """
        return self.blocks
    
    def split_blocks(self, markdown):
        """
        Splits the markdown text into a list of blocks.

        Args:
            markdown (str): The markdown text to split.

        Returns:
            list: A list of markdown blocks.
        """
        # split and clean blocks
        blocks = markdown.split("\n\n")
        blocks = list(map(lambda x : x.strip(), blocks))
        blocks = list(filter(None, blocks))
        #debug_print(f"DEBUG split blocks to: {blocks}")
        return blocks

    def parse_markdown(self, blocks):
        """
        Parses a list of markdown blocks into block objects.

        Args:
            blocks (list): A list of markdown blocks.
        """
        if blocks == []: 
            return
        debug_print("\n##########################")
        debug_print(f"Starting parsing on on {blocks}")

        for block in blocks:
            self.add_block(self.parse_block(block))

    def parse_block(self, block):
        """
        Parses a single markdown block into a block object.

        Args:
            block (str): The markdown block to parse.

        Returns:
            BlockNode: The parsed block object.
        """
        lines = block.split("\n")
        debug_print(f"DEBUG parsing block: {block}")
        
        if block.startswith("#"):
            return HeadingBlock(block)
        if block.startswith("---"):
            return RuleBlock()
        if block.startswith("```") and block.endswith("```"): #BUG: code block are allowed to have empty lines in between
            return CodeBlock(block)
        if block.startswith("- ") or block.startswith("* "): 
            for line in lines:
                if not (line.startswith("- ") or not line.startswith("* ")):
                    return ParagraphBlock(block)
            return UnorderedListBlock(block)
        if starts_with_number_dot(block):
            for line in lines:
                if not starts_with_number_dot(line):
                    return ParagraphBlock(block)
            return OrderedListBlock(block)
        if block.startswith("> "): 
            for line in lines:
                if not line.startswith(">"):
                    return ParagraphBlock(block)
            return BlockQuoteBlock(block)  

        return ParagraphBlock(block)
    
    def to_html(self):
        """
        Converts the parsed markdown blocks to HTML.

        Returns:
            str: The HTML representation of the markdown blocks.
        """
        lines = ["<div>"]
        for block in self.blocks:
            lines.append(block.to_html())
        lines.append("</div>")
        return '\n'.join(lines)



    def generate_page(self, template_path, dest_path, basepath="/"):
        """
        Generates an HTML page from the parsed markdown blocks using a template.

        Args:
            template_path (str): The path to the HTML template file.
            dest_path (str): The path to save the generated HTML file.
            basepath (str, optional): The base path for links and images. Defaults to "/".
        """
        print(f"Generation page to {dest_path} using {template_path}")
        base_dir = os.path.dirname(__file__)
        template_path = os.path.join(base_dir, template_path) 
        template_content = read_file(template_path)

        # grab title of first block. This is usually a heading. Then the heading is used. In all other cases. The type of block is used
        title = self.blocks[0].title 

        # Calculate relative path from dest_path to docs/ root for static resources
        # Count the directory depth from docs/ folder
        dest_relative = os.path.relpath(dest_path, "docs/")
        depth = dest_relative.count(os.sep)
        if depth > 0:
            # If in subdirectory, use relative path
            rel_path = "../" * depth
        else:
            # If in docs root, use current directory
            rel_path = ""
        
        final_html = template_content.replace("{{ Title }}",title).replace("{{ Content }}",self.to_html())
        # Replace static resource paths (CSS, images) with relative paths
        final_html = final_html.replace('href="/index.css"', f'href="{rel_path}index.css"')
        final_html = final_html.replace('src="/images/', f'src="{rel_path}images/')
        # Replace navigation links with basepath
        final_html = final_html.replace('href="/',f'href="{basepath}')
        debug_print(f"DEBUG: final_html: {final_html}")
        with open(dest_path, "w") as f:
            f.write(final_html)


    def print_html(self):
        """
        Prints the HTML representation of the markdown blocks to the console.
        """
        print(self.to_html())

class __BlockNode():
    """
    Base class for all block types.
    """
    def __init__(self, block):
        """
        Initializes the __BlockNode object.

        Args:
            block (str): The markdown block text.
        """
        self.text = block
        self.textnodes = TextParser(block).parse_text()
        self.html_tag = None
        self.html_item_tag = None
        self.title = self.__class__
        
    def to_html(self):
        """
        Converts the block to HTML.

        Returns:
            str: The HTML representation of the block.
        """
        result = f"<{self.html_tag}>"
        for node in self.textnodes:
            result += node.to_html()
        return result + f"</{self.html_tag}>"
   
    def to_html_list(self):
        """
        Converts a list-type block (e.g., UnorderedListBlock, OrderedListBlock) to HTML.

        Returns:
            str: The HTML representation of the list block.
        """
        first = True
        result = f"<{self.html_tag}>\n"
        for node in self.textnodes:
            if isinstance(node, ListItemNode): 
                if first:
                    result += f"  <{self.html_item_tag}>"
                    first = False
                else: 
                    result += f"</{self.html_item_tag}>\n  <{self.html_item_tag}>"
            else: result += f"{node.to_html()}"
        return result + f"</{self.html_item_tag}>\n</{self.html_tag}>"


class HeadingBlock(__BlockNode):
    """
    Represents a heading block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the HeadingBlock object.

        Args:
            block (str): The markdown heading block text.
        """
        super().__init__(block)
        self.html_tag = "h"
        self.title = ""
        self.heading_level = 0
        self.parse_heading()


    def __repr__(self):
        """
        Returns a string representation of the HeadingBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nHeading {self.title} LeveL:{self.heading_level}: {self.text})"

    def parse_heading(self):
        """
        Parses the heading text to extract the heading level and title.
        """
        # parse heading level
        self.heading_level = len(self.text.strip().split()[0])
        # remove the heading marker from the text
        self.title = self.text.strip("#").strip()

    def to_html(self):
        """
        Converts the heading block to HTML.

        Returns:
            str: The HTML representation of the heading block.
        """
        return f"<{self.html_tag}{self.heading_level}>{self.title}</{self.html_tag}{self.heading_level}>"


class ParagraphBlock(__BlockNode):
    """
    Represents a paragraph block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the ParagraphBlock object.

        Args:
            block (str): The markdown paragraph block text.
        """
        super().__init__(block)
        self.html_tag = "p"

    def __repr__(self):
        """
        Returns a string representation of the ParagraphBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nParagraph: {self.text})"

class RuleBlock(__BlockNode):
    """
    Represents a horizontal rule block in markdown.
    """
    def __init__(self):
        """
        Initializes the RuleBlock object.
        """
        pass

    def __repr__(self):
        """
        Returns a string representation of the RuleBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nRuleBlock: ---)"

    def to_html(self):
        """
        Converts the rule block to HTML.

        Returns:
            str: The HTML representation of the rule block.
        """
        return "<hr />"
    
class CodeBlock(__BlockNode):
    """
    Represents a code block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the CodeBlock object.

        Args:
            block (str): The markdown code block text.
        """
        self.text = block
        self.textnodes = self.parse_codeblock(block)
        self.html_tag = "code"
        
    def __repr__(self):
        """
        Returns a string representation of the CodeBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nCodeBlock: {self.text})"
    
    def parse_codeblock(self, block):
        """
        Parses the code block text.

        Args:
            block (str): The markdown code block text.

        Returns:
            list: A list containing a single TextNode with the code content.
        
        Raises:
            ValueError: If the code block is not well-formed.
        """
        lines = block.strip().splitlines()
        
        if not lines[0].strip().startswith("```") or not lines[-1].strip().startswith("```"):
            raise ValueError("CodeBlock not well formated")
        return [TextNode("\n".join(lines[1:-1]))]

    def to_html(self):
        """
        Converts the code block to HTML.

        Returns:
            str: The HTML representation of the code block.
        """
        return f"<pre><{self.html_tag}>\n{self.textnodes[0].to_html()}\n</{self.html_tag}></pre>"

class UnorderedListBlock(__BlockNode):
    """
    Represents an unordered list block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the UnorderedListBlock object.

        Args:
            block (str): The markdown unordered list block text.
        """
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "ul"
        self.html_item_tag = "li"
        
    def __repr__(self):
        """
        Returns a string representation of the UnorderedListBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nUnordered List: {self.textnodes})"

    def to_html(self): 
        """
        Converts the unordered list block to HTML.

        Returns:
            str: The HTML representation of the unordered list block.
        """
        return super().to_html_list()
        
class OrderedListBlock(__BlockNode):
    """
    Represents an ordered list block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the OrderedListBlock object.

        Args:
            block (str): The markdown ordered list block text.
        """
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "ol"
        self.html_item_tag = "li"
        
    def __repr__(self):
        """
        Returns a string representation of the OrderedListBlock object.

        Returns:
            str: String representation of the object.
        """
        return f"\nOrdered List: {self.textnodes})"
    
    def to_html(self):
        """
        Converts the ordered list block to HTML.

        Returns:
            str: The HTML representation of the ordered list block.
        """
        return super().to_html_list()

class BlockQuoteBlock(__BlockNode): #TODO: Does not work as expected
    """
    Represents a blockquote block in markdown.
    """
    def __init__(self, block):
        """
        Initializes the BlockQuoteBlock object.

        Args:
            block (str): The markdown blockquote block text.
        """
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "blockquote"
        self.html_item_tag = "p"
        
    def to_html(self): 
        """
        Converts the blockquote block to HTML.

        Returns:
            str: The HTML representation of the blockquote block.
        """
        return super().to_html_list()
        