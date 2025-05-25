from block import *

def main():
    print("Hello from blog!")

    md = "# Hello World\n\nThis is a **simple** paragraph.\nand another line\n\nAnother paragraph.\n\n## Subheading\n\nand some more text"

    md2 = """
Here is an image: ![dog](dog.jpg)
Another one ![cat](cat.png) in the same paragraph.

> lorem ipsum dolor **sit amet**, consectetur adipiscing elit.
> **sed do eiusmod** tempor incididunt ut labore et dolore magna aliqua.
> ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
> and more

sone some more text here.
"""

    md3 = "This _is_ a single **paragrpah** thi ![dog](dog.jpg) with some **bold text** and _some italic text_ and `some code` too."

    doc = MarkdownParser(md2)
    print("Parsed Markdown:")
    print(doc.return_blocks())

    print("\n\n")
    print(doc.to_html())

    print("###################################")


    doc.to_file("docs/output.html")

    # t = TextParser(md3)
    # print("Parsed Markdown:")
    # t.parse_text()
    


if __name__ == "__main__":
    main()
