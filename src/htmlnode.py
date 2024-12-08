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
    def __init__(self, tag, children, props=None):
        if tag is None or tag == "":
            raise ValueError("Tag cannot be empty")
        if children is None:
            raise ValueError("Children cannot be empty")

        # Convert children to list if provided
        children = list(children) if children is not None else []

        super().__init__(tag, None, children, props)

    def props_to_html(self):
        """Override parent's props_to_html to add space before each prop"""
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def to_html(self):
        if self.tag is None or self.tag == "":
            raise ValueError("Tag cannot be empty")
        if not self.children:  # Handles both None and empty list
            raise ValueError("Children cannot be empty")

        # Validate children types
        for child in self.children:
            if not isinstance(child, HTMLNode):
                raise ValueError("Children must be of type HTMLNode")

        # Generate HTML
        children_html = "".join(child.to_html() for child in self.children)
        return f'<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>'