from enum import Enum

class BlockTypes(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UL = "unordered_list"
    OL = "ordered_list"


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        props_html = ""
        if self.props:
            for key, value in self.props.items():
                props_html += " " + key + f'="{value}"'
        
        return props_html
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        return (
            f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        )
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, None)

    def to_html(self):
        if not self.tag:
            raise ValueError("No required tag was provided")
        if not self.children:
            raise ValueError("No required children provided")
        
        children_html = ""
        for child in self.children:
            children_html += child.to_html()

        return (
            f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
        )
    
def markdown_to_blocks(markdown):
    blocks = []
    parts = markdown.split("\n\n")
    for part in parts:
        if len(part) > 0:
            blocks.append(part.strip())
    return blocks

def block_to_block_type(block):
    if block.startswith("#") and block.lstrip("#").startswith(" "):
        return BlockTypes.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockTypes.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines):
        return BlockTypes.QUOTE
    if all(line.startswith(f"{i + 1}.") for i, line in enumerate(lines)):
        return BlockTypes.OL
    if all(line.startswith("*") or line.startswith("-") for line in lines):
        return BlockTypes.UL
    return BlockTypes.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    div_node = ParentNode("div", [])  # Initialize div_node with empty children list
    for block in blocks:
        if block_to_block_type(block) == BlockTypes.HEADING:
            for line in block.split("\n"):
                level = line.count("#")
                tag = f"h{level if level < 7 else 6}"
                value = line.lstrip("#").strip()
                div_node.children.append(LeafNode(tag, value))
        elif block_to_block_type(block) == BlockTypes.CODE:
            value = "\n".join(block.split("\n")[1:-1])
            code_node = ParentNode("code", [LeafNode("", value)])  # Create code_node
            div_node.children.append(ParentNode("pre", [code_node]))  # Append code_node to pre tag
        elif block_to_block_type(block) == BlockTypes.QUOTE:
            lines = block.split("\n")
            inner_children = [LeafNode("p", line.lstrip("> ").strip()) for line in lines]
            div_node.children.append(ParentNode("blockquote", inner_children))
        elif block_to_block_type(block) == BlockTypes.UL:
            lines = block.split("\n")
            items = [line.lstrip("*- ").strip() for line in lines if line.strip()]
            inner_children = [LeafNode("li", item) for item in items]
            div_node.children.append(ParentNode("ul", inner_children))
        elif block_to_block_type(block) == BlockTypes.OL:
            lines = block.split("\n")
            items = [line.split(".", 1)[1].strip() for line in lines if line.strip()]
            inner_children = [LeafNode("li", item) for item in items]
            div_node.children.append(ParentNode("ol", inner_children))
        else:
            div_node.children.append(LeafNode("p", block.strip()))
    return div_node






    
        