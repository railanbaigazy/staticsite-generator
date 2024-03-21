import re
from htmlnode import LeafNode
from enum import Enum

class TextTypes(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text 
            and self.text_type == other.text_type
            and self.url == other.url
        )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    

def text_node_to_html(text_node):
    if text_node.text_type == TextTypes.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextTypes.BOLD:
        return LeafNode("b", text_node.text)
    elif text_node.text_type == TextTypes.ITALIC:
        return LeafNode("i", text_node.text)
    elif text_node.text_type == TextTypes.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextTypes.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextTypes.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Such text type is not supported!")


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    if delimiter == "":
        return old_nodes

    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.TEXT:
            parts = node.text.split(delimiter)

            # handling no matching delimiter
            if len(parts) % 2 == 0:
                raise ValueError("No matching closing delimiter")
            
            for i, part in enumerate(parts):
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextTypes.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        else:
            new_nodes.append(node)
        
    return new_nodes


def extract_markdown_images(text):
    images = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    return links

def split_nodes(old_nodes, extract_func, text_type):
    new_nodes = []
    exclamation_mark = '!' if text_type == TextTypes.IMAGE else ''
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.TEXT:
            elements = extract_func(node.text)
            if elements:
                parts = re.split(f"{exclamation_mark}\[.*?\]\(.*?\)", node.text)
                for i, part in enumerate(parts):
                    if part:
                        new_nodes.append(TextNode(part, TextTypes.TEXT))
                    if i < len(elements):
                        new_nodes.append(TextNode(elements[i][0], text_type, elements[i][1]))
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes


def split_nodes_image(old_nodes):
    return split_nodes(old_nodes, extract_markdown_images, TextTypes.IMAGE)

def split_nodes_link(old_nodes):
    return split_nodes(old_nodes, extract_markdown_links, TextTypes.LINK)

def text_to_textnodes(text):
    nodes = [TextNode(text, TextTypes.TEXT)]
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextTypes.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextTypes.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextTypes.CODE)
    return nodes
