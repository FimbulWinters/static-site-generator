import unittest

from src.htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def setUp(self):
        # Create some common test nodes for reuse across tests
        self.empty_node = HTMLNode()
        self.paragraph = HTMLNode(tag="p", value="Hello, world!")
        self.link = HTMLNode(
            tag="a", 
            value="Click me",
            props={"href": "https://example.com", "target": "_blank"}
        )
        self.nested = HTMLNode(
            tag="div",
            children=[
                HTMLNode(tag="p", value="First child"),
                HTMLNode(tag="p", value="Second child")
            ]
        )

    def test_initialization_empty(self):
        # Test that a node can be created with no parameters
        self.assertIsNone(self.empty_node.tag)
        self.assertIsNone(self.empty_node.value)
        self.assertIsNone(self.empty_node.children)
        self.assertIsNone(self.empty_node.props)

    def test_initialization_with_values(self):
        # Test initialization with all parameters
        node = HTMLNode(
            tag="div",
            value="content",
            children=[HTMLNode(tag="p")],
            props={"class": "container"}
        )
        self.assertEqual(node.tag, "div")
        self.assertEqual(node.value, "content")
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.props["class"], "container")

    def test_to_html_raises_not_implemented(self):
        # Test that to_html raises NotImplementedError
        with self.assertRaises(NotImplementedError):
            self.empty_node.to_html()

    def test_props_to_html_with_link_props(self):
        # Test props_to_html with link properties
        expected = ' href="https://example.com" target="_blank"'
        props = {"href": "https://example.com", "target":"blank"}
        node = HTMLNode(props=props)
        self.assertEqual(node.props_to_html(), expected)

    def test_children_mutability(self):
        # Test that modifying the children list after initialization works
        node = HTMLNode(children=[])
        node.children.append(HTMLNode(tag="p"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.children[0].tag, "p")

    def test_props_mutability(self):
        # Test that modifying props after initialization works
        node = HTMLNode(props={})
        node.props["class"] = "new-class"
        self.assertEqual(node.props["class"], "new-class")

    def test_nested_structure(self):
        # Test that nested structure is maintained correctly
        self.assertEqual(len(self.nested.children), 2)
        self.assertEqual(self.nested.children[0].value, "First child")
        self.assertEqual(self.nested.children[1].value, "Second child")

    def test_empty_children_list(self):
        # Test initialization with empty children list
        node = HTMLNode(children=[])
        self.assertEqual(node.children, [])

    def test_empty_props_dict(self):
        # Test initialization with empty props dictionary
        node = HTMLNode(props={})
        self.assertEqual(node.props, {})

if __name__ == "__main__":
    unittest.main()