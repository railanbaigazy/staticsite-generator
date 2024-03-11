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
        