class HTMLNode:
    def __init__(self, tag = None , value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    def __eq__(self, other):
        return (self.tag == other.tag and
                self.value == other.value and
                self.children == other.children and
                self.props == other.props)
        
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f'{key}="{value}"' for key, value in self.props.items()])
    
    def __repr__(self):
       return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag, value):
        super().__init__(tag, value)

    def to_html(self):
        if self.value == 0 or self.value is None:
            raise ValueError
        if self.tag is None or self.tag == 0:
            return f'{self.value}'
        else:
                return f'<{self.tag}>{self.value}</{self.tag}>'

class ParentNode(HTMLNode):

    def __init__(self, tag, children, props = None):
        super().__init__(tag, children, props)

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Tag cannot be empty")
        if self.children is None or self.children == []:
            raise ValueError("Children cannot be empty")
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be of type HTMLNode")
        return f'<{self.tag}{self.props_to_html()}>{"".join([child.to_html() for child in self.children])}</{self.tag}>'