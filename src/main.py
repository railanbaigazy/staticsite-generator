from textnode import TextNode
from htmlnode import HTMLNode, ParentNode, LeafNode


def main():
    txtnod = TextNode("Text check", "bold", "https://github.com")
    htmlnod = HTMLNode("a", "Text check", None, {"href": "https://www.google.com"})
    parentnod = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)

    print(txtnod)
    print(htmlnod)
    print(parentnod.to_html())


main()