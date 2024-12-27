from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("No tag given")
        if not self.children or self.children == []:
            raise ValueError("No children given")

        props_html = self.props_to_html() if self.props else ""
        html = f"<{self.tag}{props_html}>"

        for child in self.children:
            html += child.to_html()

        html += f"</{self.tag}>"
        return html
