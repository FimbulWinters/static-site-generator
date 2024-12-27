import unittest
from leaf_node import LeafNode
from htmlnode import HTMLNode

class TestLeafNode(unittest.TestCase):
    def setUp(self):
        # Create common test instances for reuse
        self.text_only = LeafNode(value="Just some text")
        self.paragraph = LeafNode(tag="p", value="Hello, world!")
        self.link = LeafNode(
            tag="a", 
            value="Click me",
            props={"href": "https://example.com", "target": "blank"}
        )

    def test_initialization(self):
        # Test that LeafNode initializes with correct values and no children
        node = LeafNode(tag="span", value="test", props={"class": "highlight"})
        
        # Verify all properties are set correctly
        self.assertEqual(node.tag, "span")
        self.assertEqual(node.value, "test")
        self.assertEqual(node.props["class"], "highlight")
        # Verify children is None as specified in LeafNode.__init__
        self.assertIsNone(node.children)

    def test_empty_initialization(self):
        # Test initialization with no parameters
        node = LeafNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_text_only(self):
        # Test converting a text-only node (no tag) to HTML
        self.assertEqual(
            self.text_only.to_html(),
            "Just some text",
            "Text-only nodes should return just their value"
        )

    def test_to_html_with_tag(self):
        # Test converting a basic paragraph node to HTML
        expected = "<p>Hello, world!</p>"
        self.assertEqual(
            self.paragraph.to_html(),
            expected,
            "Node with tag should be wrapped in HTML tags"
        )

    def test_to_html_with_props(self):
        # Test converting a node with properties to HTML
        expected = '<a href="https://example.com" target="_blank">Click me</a>'
        self.assertEqual(
            self.link.to_html(),
            expected,
            "Node with props should include them in the HTML tag"
        )

    def test_to_html_no_value(self):
        # Test that to_html raises ValueError when no value is provided
        node = LeafNode(tag="p")
        with self.assertRaises(ValueError) as context:
            node.to_html()
        self.assertEqual(
            str(context.exception),
            "No value supplied",
            "Should raise ValueError with appropriate message"
        )

    def test_inheritance(self):
        # Test that LeafNode is properly inheriting from HTMLNode
        node = LeafNode()
        self.assertTrue(
            isinstance(node, HTMLNode),
            "LeafNode should be an instance of HTMLNode"
        )

    def test_children_always_none(self):
        # Test that children parameter is ignored and always set to None
        node = LeafNode(tag="p", value="test", props={"class": "test"})
        self.assertIsNone(
            node.children,
            "LeafNode should never have children"
        )
        
    def test_to_html_special_characters(self):
        # Test handling of special characters in value
        node = LeafNode(tag="p", value="Hello & goodbye")
        expected = "<p>Hello & goodbye</p>"
        self.assertEqual(
            node.to_html(),
            expected,
            "Should handle special characters correctly"
        )

    def test_to_html_empty_props(self):
        # Test that empty props produce clean HTML
        node = LeafNode(tag="span", value="test")
        expected = "<span>test</span>"
        self.assertEqual(
            node.to_html(),
            expected,
            "Empty props should result in clean HTML tags"
        )

if __name__ == "__main__":
    unittest.main()