from helper import debug_print, starts_with_number_dot, read_file, LOG_LEVEL_DEBUG
from text import *
import os
       

class MarkdownParser():
    def __init__(self, markdown):
        self.n_blocks = 0
        self.blocks = []
        self.parse_markdown(self.split_blocks(markdown))

    def add_block(self, block):
        self.blocks.append(block)
        self.n_blocks += 1

    def return_blocks(self):
        return self.blocks
    
    def split_blocks(self, markdown):
        # split and clean blocks
        blocks = markdown.split("\n\n")
        blocks = list(map(lambda x : x.strip(), blocks))
        blocks = list(filter(None, blocks))
        #debug_print(f"DEBUG split blocks to: {blocks}", LOG_LEVEL_DEBUG)
        return blocks

    def parse_markdown(self, blocks):
        if blocks == []: 
            return
        debug_print("\n##########################", LOG_LEVEL_DEBUG)
        debug_print(f"Starting parsing on on {blocks}", LOG_LEVEL_DEBUG)

        for block in blocks:
            self.add_block(self.parse_block(block))

    def parse_block(self, block):
        lines = block.split("\n")
        debug_print(f"DEBUG parsing block: {block}", LOG_LEVEL_DEBUG)
        
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
        lines = ["<div>"]
        for block in self.blocks:
            lines.append(block.to_html())
        lines.append("</div>")
        return '\n'.join(lines)



    def generate_page(self, template_path, dest_path, basepath="/"):
        print(f"Generation page to {dest_path} using {template_path}")
        base_dir = os.path.dirname(__file__)
        template_path = os.path.join(base_dir, template_path) 
        template_content = read_file(template_path)

        # grab title of first block. This is usually a heading. Then the heading is used. In all other cases. The type of block is used
        title = self.blocks[0].title 

        final_html = template_content.replace("{{ Title }}",title).replace("{{ Content }}",self.to_html())
        final_html = final_html.replace('href="/',f'href="{basepath}').replace('src="/',f'src="{basepath}')
        debug_print(f"DEBUG: final_html: {final_html}", LOG_LEVEL_DEBUG)
        with open(dest_path, "w") as f:
            f.write(final_html)


    def print_html(self):
        print(self.to_html())

class __BlockNode():
    def __init__(self, block):
        self.text = block
        self.textnodes = TextParser(block).parse_text()
        self.html_tag = None
        self.html_item_tag = None
        self.title = self.__class__
        
    def to_html(self):
        result = f"<{self.html_tag}>"
        for node in self.textnodes:
            result += node.to_html()
        return result + f"</{self.html_tag}>"
   
    def to_html_list(self):
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
    def __init__(self, block):
        super().__init__(block)
        self.html_tag = "h"
        self.title = ""
        self.heading_level = 0
        self.parse_heading()


    def __repr__(self):
        return f"\nHeading {self.title} LeveL:{self.heading_level}: {self.text})"

    def parse_heading(self):
        # parse heading level
        self.heading_level = len(self.text.strip().split()[0])
        # remove the heading marker from the text
        self.title = self.text.strip("#").strip()

    def to_html(self):
        return f"<{self.html_tag}{self.heading_level}>{self.title}</{self.html_tag}{self.heading_level}>"


class ParagraphBlock(__BlockNode):
    def __init__(self, block):
        super().__init__(block)
        self.html_tag = "p"

    def __repr__(self):
        return f"\nParagraph: {self.text})"

class RuleBlock(__BlockNode):
    def __init__(self):
        pass

    def __repr__(self):
        return f"\nRuleBlock: ---)"

    def to_html(self):
        return "<hr />"
    
class CodeBlock(__BlockNode):
    def __init__(self, block):
        self.text = block
        self.textnodes = self.parse_codeblock(block)
        self.html_tag = "code"
        
    def __repr__(self):
        return f"\nCodeBlock: {self.text})"
    
    def parse_codeblock(self, block):
        lines = block.strip().splitlines()
        
        if not lines[0].strip().startswith("```") or not lines[-1].strip().startswith("```"):
            raise ValueError("CodeBlock not well formated")
        return [TextNode("\n".join(lines[1:-1]))]

    def to_html(self):
        return f"<pre><{self.html_tag}>\n{self.textnodes[0].to_html()}\n</{self.html_tag}></pre>"

class UnorderedListBlock(__BlockNode):
    def __init__(self, block):
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "ul"
        self.html_item_tag = "li"
        
    def __repr__(self):
        return f"\nUnordered List: {self.textnodes})"

    def to_html(self): 
        return super().to_html_list()
        
class OrderedListBlock(__BlockNode):
    def __init__(self, block):
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "ol"
        self.html_item_tag = "li"
        
    def __repr__(self):
        return f"\nOrdered List: {self.textnodes})"
    
    def to_html(self):
        return super().to_html_list()

class BlockQuoteBlock(__BlockNode): #TODO: Does not work as expected
    def __init__(self, block):
        self.text = block
        self.textnodes = TextParser(block).parse_text_and_list()
        self.html_tag = "blockquote"
        self.html_item_tag = "p"
        
    def to_html(self): 
        return super().to_html_list()
        