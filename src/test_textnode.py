import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def setUp(self):
        # Create some common test nodes that we'll use across multiple tests
        self.bold_node = TextNode("Bold text", TextType.Bold)
        self.italic_node = TextNode("Italic text", TextType.Italic)
        self.link_node = TextNode(
            "Link text", TextType.Links, "https://example.com")

    def test_eq_identical_nodes(self):
        # Test that two nodes with the same content are equal
        node1 = TextNode("This is a text node", TextType.Bold)
        node2 = TextNode("This is a text node", TextType.Bold)
        self.assertEqual(node1, node2)

    def test_eq_different_text(self):
        # Test that nodes with different text are not equal
        node1 = TextNode("First text", TextType.Text)
        node2 = TextNode("Second text", TextType.Text)
        self.assertNotEqual(node1, node2)

    def test_eq_different_types(self):
        # Test that nodes with same text but different types are not equal
        node1 = TextNode("Same text", TextType.Bold)
        node2 = TextNode("Same text", TextType.Italic)
        self.assertNotEqual(node1, node2)

    def test_eq_different_urls(self):
        # Test that link nodes with different URLs are not equal
        node1 = TextNode("Link text", TextType.Links, "https://example.com")
        node2 = TextNode("Link text", TextType.Links, "https://other.com")
        self.assertNotEqual(node1, node2)

    def test_repr_without_url(self):
        # Test string representation of a node without URL
        node = TextNode("Simple text", TextType.Text)
        expected = "TextNode(Simple text, Text, None)"
        self.assertEqual(repr(node), expected)

    def test_repr_with_url(self):
        # Test string representation of a node with URL
        node = TextNode("Link text", TextType.Links, "https://example.com")
        expected = "TextNode(Link text, Links, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_url_optional(self):
        # Test that URL is optional for non-link nodes
        node = TextNode("Code block", TextType.Code)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
