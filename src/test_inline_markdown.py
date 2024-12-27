import unittest


from textnode import TextNode, TextType
from utils import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_Bold(self):
        node = TextNode("This is Text with a **Bolded** word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is Text with a ", TextType.Text),
                TextNode("Bolded", TextType.Bold),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )

    def test_delim_Bold_double(self):
        node = TextNode(
            "This is Text with a **Bolded** word and **another**", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is Text with a ", TextType.Text),
                TextNode("Bolded", TextType.Bold),
                TextNode(" word and ", TextType.Text),
                TextNode("another", TextType.Bold),
            ],
            new_nodes,
        )

    def test_delim_Bold_multiword(self):
        node = TextNode(
            "This is Text with a **Bolded word** and **another**", TextType.Text
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        self.assertListEqual(
            [
                TextNode("This is Text with a ", TextType.Text),
                TextNode("Bolded word", TextType.Bold),
                TextNode(" and ", TextType.Text),
                TextNode("another", TextType.Bold),
            ],
            new_nodes,
        )

    def test_delim_Italic(self):
        node = TextNode("This is Text with an *Italic* word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "*", TextType.Italic)
        self.assertListEqual(
            [
                TextNode("This is Text with an ", TextType.Text),
                TextNode("Italic", TextType.Italic),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )

    def test_delim_Bold_and_Italic(self):
        node = TextNode("**Bold** and *Italic*", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "**", TextType.Bold)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.Italic)
        self.assertListEqual(
            [
                TextNode("Bold", TextType.Bold),
                TextNode(" and ", TextType.Text),
                TextNode("Italic", TextType.Italic),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is Text with a `code block` word", TextType.Text)
        new_nodes = split_nodes_delimiter([node], "`", TextType.Code)
        self.assertListEqual(
            [
                TextNode("This is Text with a ", TextType.Text),
                TextNode("code block", TextType.Code),
                TextNode(" word", TextType.Text),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
