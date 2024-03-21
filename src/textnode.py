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


def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextTypes.TEXT:
            images = extract_markdown_images(node.text)
            if images:
                parts = []
                for image in images:   
                    if parts:
                        last_part = parts[len(parts) - 1].split(f"![{image[0]}]({image[1]})")
                        new_parts = parts[:len(parts) - 1] + [""] + last_part
                        parts = new_parts
                    else:
                        new_parts = node.text.split(f"![{image[0]}]({image[1]})")
                        parts = new_parts

                image_count = 0
                for i, part in enumerate(parts):
                    if i % 2 == 0:
                        new_nodes.append(TextNode(part, TextTypes.TEXT))
                    else:
                        new_nodes.append(TextNode(images[image_count][0], TextTypes.IMAGE, images[image_count][1]))
                        image_count += 1
            else:
                new_nodes.append(node)
        else:
            new_nodes.append(node)
    return new_nodes
            

def split_nodes_link(old_nodes):
    pass