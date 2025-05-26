import re
from helper import debug_print, starts_with_number_dot

class TextParser():
    def __init__(self, text):
        self.text = text
        self.textnodes = []

    def parse_text(self):
        for line in self.text.splitlines():
            f_nodes = []
            if line.strip() == "":
                continue
            debug_print(f"DEBUG parsing line: {line}")

            debug_print(f"DEBUG bold: {self.extract_bold(line)}")
            debug_print(f"DEBUG italic: {self.extract_italic(line)}")
            debug_print(f"DEBUG inline_code: {self.extract_inline_code(line)}")
            debug_print(f"DEBUG links: {self.extract_links(line)}")
            debug_print(f"DEBUG images: {self.extract_images(line)}")

            f_nodes.extend(self.extract_bold(line))
            f_nodes.extend(self.extract_italic(line))
            f_nodes.extend(self.extract_inline_code(line))
            f_nodes.extend(self.extract_links(line))
            f_nodes.extend(self.extract_images(line))
            #f_nodes.extend(self.extract_newlines(line)) #TODO: remove?!

            f_nodes = sorted(f_nodes,key=lambda x: x[0])
            debug_print(f"DEBUG: f_nodes {f_nodes}")

            marker = 0
            for node in f_nodes:
                if node[0] != marker:
                    self.textnodes.append(TextNode(line[marker:node[0]])) 
                node_text = line[node[0]:node[0]+len(node[1])]
                if node_text.startswith("!["):
                    self.textnodes.append(ImageNode(node_text))
                elif node_text.startswith("["):
                    self.textnodes.append(LinkNode(node_text))
                elif node_text.startswith("`"):
                    self.textnodes.append(CodeNode(node_text))
                elif node_text.startswith("**"):
                    self.textnodes.append(BoldNode(node_text))
                elif node_text.startswith("_"):
                    self.textnodes.append(ItalicNode(node_text))
                else:
                    raise Exception("Unknown error in parsing")
                marker = node[0] + len(node[1])
            
            # if there is something left after the last node
            if marker != len(line):
                self.textnodes.append(TextNode(line[marker:]))

        debug_print(f"DEBUG: textnodes: {self.textnodes}")
        return self.textnodes
    
    
    def parse_list(self):
        result = []
        for node in self.textnodes:
            if node.text.startswith("- ") or node.text.startswith("* ") or node.text.startswith("> "):
                result.append(ListItemNode())
                result.append(TextNode(node.text[2:])) 
            elif starts_with_number_dot(node.text): 
                 result.append(ListItemNode())
                 result.append(TextNode(node.text.split('.', 1)[1].strip()))
            else:
                result.append(node)
        return result  

    def parse_text_and_list(self):
        self.parse_text()
        return self.parse_list()

    def extract_markdown_images(self, markdown):
        pattern = r'!\[.*?\]\(.*?\)'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]


    def extract_images(self, markdown):
        pattern = r'!\[.*?\]\(.*?\)'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_links(self, markdown):
        pattern = r'(?<!!)\[(.*?)\]\((.*?)\)' 
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_bold(self, markdown):
        pattern = r'(\*\*|__)(.+?)\1'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_italic(self, markdown):
        pattern = r'_(.+?)_'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_inline_code(self, markdown):
        pattern = r'`([^`\n]+?)`'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_newlines(self, markdown): ##TODO: remove?
        pattern = r'\n'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]


class __Node():
    def __init__(self, text):
        self.text = text
        self.tag = None

    def to_html(self):
        return f"<{self.tag}>{self.text}</{self.tag}>"
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.text})"

class TextNode(__Node):
    def __init__(self, text):
        super().__init__(text) 

    def to_html(self):
        return self.text

class BoldNode(__Node):
    def __init__(self, text):
        super().__init__(text)
        self.text = text.strip("**")
        #self.tag = "strong"
        self.tag = "b"


class ItalicNode(__Node):
    def __init__(self, text):
        super().__init__(text)
        self.text = text.strip("_")
        self.tag = "i"


class CodeNode(__Node):
    def __init__(self, text):
        super().__init__(text)
        self.text = text.strip("`")
        self.tag = "code"


class LinkNode(__Node):
    def __init__(self, text):
        super().__init__(text)
        self.tag = "a"
        self.text, self.url = self.extract_url()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text} - {self.url})"

    def to_html(self):
        return f'<{self.tag} href="{self.url}">{self.text}</{self.tag}>'
    
    def extract_url(self): 
        pattern = r'\[(.*?)\]\((.*?)\)'
        match = re.match(pattern, self.text)
        if match:
            text, url = match.groups()
            return text, url
        raise Exception("Invalid link format")

class ImageNode(__Node):
    def __init__(self, text):
        super().__init__(text)
        self.tag = "img"
        self.text, self.url = self.extract_url()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text} - {self.url})"
    
    def to_html(self):
        return f'<{self.tag} src="{self.url}" alt="{self.text}" />'

    def extract_url(self): 
        debug_print(f"DEBUG: extracting url: {self.text}")
        pattern = r'!\[(.*?)\]\((.*?)\)'
        match = re.match(pattern, self.text)
        debug_print(f"DEBUG: match: {match}")
        if match:
            text, url = match.groups()
            debug_print(f"DEBUG: extracted url: {text} and {url}")
            return text, url
        raise Exception("Invalid image format")
    
class ListItemNode(__Node):
    def __init__(self):
        self.text = ""
        self.tag = "li"

    def to_html(self):
        return ""
    
