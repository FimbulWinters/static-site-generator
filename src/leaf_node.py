from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self,tag = None, value = None, props = None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError("No value supplied")
        elif not self.tag:
            return self.value
        else:
            props_html = ""
            print(self.props)
            if self.props:
                props_html = self.props_to_html()

            return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
        