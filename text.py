import re
from helper import debug_print, starts_with_number_dot

class TextParser():
    """
    Parses a string of text and extracts various markdown elements.
    """
    def __init__(self, text):
        """
        Initializes the TextParser object.

        Args:
            text (str): The text to parse.
        """
        self.text = text
        self.textnodes = []

    def parse_text(self):
        """
        Parses the text and converts it into a list of Node objects.

        The parsing process identifies and creates nodes for plain text,
        bold text, italic text, inline code, links, and images.

        Returns:
            list: A list of Node objects representing the parsed text.
        """
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
        """
        Converts parsed text nodes into a list structure.

        Identifies list items (unordered and ordered) and wraps their
        content with ListItemNode.

        Returns:
            list: A list of Node objects with list items identified.
        """
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
        """
        Parses text and then processes it for list structures.

        Returns:
            list: A list of Node objects representing the parsed text with list items.
        """
        self.parse_text()
        return self.parse_list()

    def extract_markdown_images(self, markdown):
        """
        Extracts markdown images from a string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched image string.
        """
        pattern = r'!\[.*?\]\(.*?\)'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]


    def extract_images(self, markdown):
        """
        Extracts images from a markdown string. (Currently a duplicate of extract_markdown_images)

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched image string.
        """
        pattern = r'!\[.*?\]\(.*?\)'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_links(self, markdown):
        """
        Extracts links from a markdown string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched link string.
        """
        pattern = r'(?<!!)\[(.*?)\]\((.*?)\)' 
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_bold(self, markdown):
        """
        Extracts bold text from a markdown string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched bold text string.
        """
        pattern = r'(\*\*|__)(.+?)\1'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_italic(self, markdown):
        """
        Extracts italic text from a markdown string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched italic text string.
        """
        pattern = r'_(.+?)_'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_inline_code(self, markdown):
        """
        Extracts inline code from a markdown string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched inline code string.
        """
        pattern = r'`([^`\n]+?)`'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]

    def extract_newlines(self, markdown): ##TODO: remove?
        """
        Extracts newline characters from a markdown string.

        Args:
            markdown (str): The markdown string.

        Returns:
            list: A list of tuples, where each tuple contains the
                  start index and the matched newline character.
        """
        pattern = r'\n'
        matches = re.finditer(pattern, markdown)
        return [(match.start(), match.group(0)) for match in matches]


class __Node():
    """
    Base class for all text nodes.
    """
    def __init__(self, text):
        """
        Initializes the __Node object.

        Args:
            text (str): The text content of the node.
        """
        self.text = text
        self.tag = None

    def to_html(self):
        """
        Converts the node to its HTML representation.

        Returns:
            str: The HTML representation of the node.
        """
        return f"<{self.tag}>{self.text}</{self.tag}>"
    
    def __repr__(self):
        """
        Returns a string representation of the __Node object.

        Returns:
            str: String representation of the object.
        """
        return f"{self.__class__.__name__}({self.text})"

class TextNode(__Node):
    """
    Represents a plain text node.
    """
    def __init__(self, text):
        """
        Initializes the TextNode object.

        Args:
            text (str): The text content of the node.
        """
        super().__init__(text) 

    def to_html(self):
        """
        Converts the text node to its HTML representation (which is just the text itself).

        Returns:
            str: The text content of the node.
        """
        return self.text

class BoldNode(__Node):
    """
    Represents a bold text node.
    """
    def __init__(self, text):
        """
        Initializes the BoldNode object.

        Args:
            text (str): The bold text content (e.g., "**bold text**").
        """
        super().__init__(text)
        self.text = text.strip("**")
        #self.tag = "strong"
        self.tag = "b"


class ItalicNode(__Node):
    """
    Represents an italic text node.
    """
    def __init__(self, text):
        """
        Initializes the ItalicNode object.

        Args:
            text (str): The italic text content (e.g., "_italic text_").
        """
        super().__init__(text)
        self.text = text.strip("_")
        self.tag = "i"


class CodeNode(__Node):
    """
    Represents an inline code node.
    """
    def __init__(self, text):
        """
        Initializes the CodeNode object.

        Args:
            text (str): The inline code content (e.g., "`code`").
        """
        super().__init__(text)
        self.text = text.strip("`")
        self.tag = "code"


class LinkNode(__Node):
    """
    Represents a link node.
    """
    def __init__(self, text):
        """
        Initializes the LinkNode object.

        Args:
            text (str): The markdown link string (e.g., "[link text](url)").
        """
        super().__init__(text)
        self.tag = "a"
        self.text, self.url = self.extract_url()

    def __repr__(self):
        """
        Returns a string representation of the LinkNode object.

        Returns:
            str: String representation of the object.
        """
        return f"{self.__class__.__name__}({self.text} - {self.url})"

    def to_html(self):
        """
        Converts the link node to its HTML representation.

        Returns:
            str: The HTML representation of the link.
        """
        return f'<{self.tag} href="{self.url}">{self.text}</{self.tag}>'
    
    def extract_url(self): 
        """
        Extracts the text and URL from the markdown link string.

        Returns:
            tuple: A tuple containing the link text and URL.
        
        Raises:
            Exception: If the link format is invalid.
        """
        pattern = r'\[(.*?)\]\((.*?)\)'
        match = re.match(pattern, self.text)
        if match:
            text, url = match.groups()
            return text, url
        raise Exception("Invalid link format")

class ImageNode(__Node):
    """
    Represents an image node.
    """
    def __init__(self, text):
        """
        Initializes the ImageNode object.

        Args:
            text (str): The markdown image string (e.g., "![alt text](url)").
        """
        super().__init__(text)
        self.tag = "img"
        self.text, self.url = self.extract_url()

    def __repr__(self):
        """
        Returns a string representation of the ImageNode object.

        Returns:
            str: String representation of the object.
        """
        return f"{self.__class__.__name__}({self.text} - {self.url})"
    
    def to_html(self):
        """
        Converts the image node to its HTML representation.

        Returns:
            str: The HTML representation of the image.
        """
        return f'<{self.tag} src="{self.url}" alt="{self.text}" />'

    def extract_url(self): 
        """
        Extracts the alt text and URL from the markdown image string.

        Returns:
            tuple: A tuple containing the alt text and URL.
        
        Raises:
            Exception: If the image format is invalid.
        """
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
    """
    Represents a list item node.
    This node is a marker and doesn't have text content itself;
    the content is handled by subsequent TextNodes.
    """
    def __init__(self):
        """
        Initializes the ListItemNode object.
        """
        self.text = ""
        self.tag = "li"

    def to_html(self):
        """
        Converts the list item node to its HTML representation.
        For ListItemNode, this is an empty string as the `<li>` tags are handled
        by the parent list block's `to_html_list` method.

        Returns:
            str: An empty string.
        """
        return ""
    
