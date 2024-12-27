from enum import Enum

from leaf_node import LeafNode


class TextType(Enum):
    Text = "Text"
    Bold = "Bold"
    Italic = "Italic"
    Code = "Code"
    Links = "Links"
    Images = "Images"


class TextNode():
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other_node):
        if self.text == other_node.text and self.text_type == other_node.text_type and self.url == other_node.url:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(self):
        match(self.text_type):
            case TextType.Text:
                return LeafNode(None, self.text)
            case TextType.Bold:
                return LeafNode("b", self.text)
            case TextType.Italic:
                return LeafNode('i', self.text)
            case TextType.Code:
                return LeafNode("code", self.text)
            case TextType.Links:
                return LeafNode("a", self.text, {"href": self.url})
            case TextType.Images:
                return LeafNode("img", None, {"src": self.url, "alt": self.value})
            case _:
                raise ValueError("No or incorrect text type given")
