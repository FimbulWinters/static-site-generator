import unittest
from leaf_node import LeafNode
from parent_node import ParentNode


class TestParentNode(unittest.TestCase):
    def test_simple_parent(self):
        child = LeafNode("p", "Hello")
        parent = ParentNode("div", [child])
        expected = "<div><p>Hello</p></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_eg(self):
        node = ParentNode("p",
                          [
                              LeafNode("b", "Bold text"),
                              LeafNode(None, "Normal text"),
                              LeafNode("i", "italic text"),
                              LeafNode(None, "Normal text"),
                          ],)
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        self.assertEqual(node.to_html(), expected)

    def test_nested_structure(self):
        inner_p = LeafNode("p", "World")
        inner_div = ParentNode("div", [inner_p])
        first_p = LeafNode("p", "Hello")
        outer_div = ParentNode("div", [first_p, inner_div])
        expected = "<div><p>Hello</p><div><p>World</p></div></div>"
        self.assertEqual(outer_div.to_html(), expected)

    def test_empty_children_list(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_no_tag_error(self):
        with self.assertRaises(ValueError):
            ParentNode(children=[LeafNode("p", "test")]).to_html()

    def test_no_children_error(self):
        with self.assertRaises(ValueError):
            ParentNode("div").to_html()


if __name__ == "__main__":
    unittest.main()
