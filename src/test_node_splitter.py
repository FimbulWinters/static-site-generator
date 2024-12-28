
import unittest
from textnode import TextNode, TextType
from utils import split_nodes_image


class TestNodeSplitter(unittest.TestCase):
    def test_single_image(self):
        """Test splitting a node with a single image"""
        input_node = TextNode(
            "Hello ![alt text](image.jpg) world",
            TextType.TEXT
        )
        result = split_nodes_image([input_node])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "Hello ")
        self.assertEqual(result[0].text_type, TextType.TEXT)
        self.assertEqual(result[1].text, "alt text")
        self.assertEqual(result[1].text_type, TextType.IMAGES)
        self.assertEqual(result[1].url, "image.jpg")
        self.assertEqual(result[2].text, " world")
        self.assertEqual(result[2].text_type, TextType.TEXT)

    def test_multiple_images(self):
        """Test splitting a node with multiple images"""
        input_node = TextNode(
            "Start ![first](img1.jpg) middle ![second](img2.jpg) end",
            TextType.TEXT
        )
        result = split_nodes_image([input_node])

        self.assertEqual(len(result), 5)
        self.assertEqual(result[0].text, "Start ")
        self.assertEqual(result[1].text, "first")
        self.assertEqual(result[1].url, "img1.jpg")
        self.assertEqual(result[2].text, " middle ")
        self.assertEqual(result[3].text, "second")
        self.assertEqual(result[3].url, "img2.jpg")
        self.assertEqual(result[4].text, " end")

    def test_no_images(self):
        """Test node with no images"""
        input_node = TextNode(
            "Just plain text here",
            TextType.TEXT
        )
        result = split_nodes_image([input_node])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].text, "Just plain text here")
        self.assertEqual(result[0].text_type, TextType.TEXT)

    def test_empty_node(self):
        """Test empty node"""
        input_node = TextNode("", TextType.TEXT)
        result = split_nodes_image([input_node])

        self.assertEqual(len(result), 0)

    def test_multiple_nodes(self):
        """Test list with multiple nodes"""
        nodes = [
            TextNode("First ![img](test.jpg) text", TextType.TEXT),
            TextNode("Second text", TextType.TEXT),
            TextNode("Third ![img](another.jpg) text", TextType.TEXT)
        ]
        result = split_nodes_image(nodes)

        self.assertEqual(len(result), 7)
        self.assertEqual(result[0].text, "First ")
        self.assertEqual(result[1].text, "img")
        self.assertEqual(result[1].url, "test.jpg")
        self.assertEqual(result[2].text, " text")
        self.assertEqual(result[3].text, "Second text")

    def test_non_text_node(self):
        """Test that non-text nodes are preserved"""
        nodes = [
            TextNode("![img](test.jpg)", TextType.TEXT),
            TextNode("Already an image", TextType.IMAGES, "existing.jpg")
        ]
        result = split_nodes_image(nodes)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].text, "img")
        self.assertEqual(result[0].url, "test.jpg")
        self.assertEqual(result[1].text, "Already an image")
        self.assertEqual(result[1].url, "existing.jpg")

    def test_image_at_start_end(self):
        """Test images at the start and end of text"""
        input_node = TextNode(
            "![start](start.jpg) middle ![end](end.jpg)",
            TextType.TEXT
        )
        result = split_nodes_image([input_node])

        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].text, "start")
        self.assertEqual(result[0].url, "start.jpg")
        self.assertEqual(result[1].text, " middle ")
        self.assertEqual(result[2].text, "end")
        self.assertEqual(result[2].url, "end.jpg")


if __name__ == '__main__':
    unittest.main()
