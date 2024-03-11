from textnode import TextNode
from htmlnode import HTMLNode


def main():
    txtnod = TextNode("Text check", "bold", "https://github.com")
    htmlnod = HTMLNode("a", "Text check", None, {"href": "https://www.google.com"})
    print(txtnod)
    print(htmlnod)


main()