import unittest
import re


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


class TestMarkdownExtractors(unittest.TestCase):
    def test_extract_images_basic(self):
        text = "Here's an image ![alt text](image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('alt text', 'image.jpg')])

    def test_extract_images_multiple(self):
        text = """
        First image ![first](img1.png)
        Second image ![second](img2.jpg)
        """
        result = extract_markdown_images(text)
        self.assertEqual(
            result, [('first', 'img1.png'), ('second', 'img2.jpg')])

    def test_extract_images_with_paths(self):
        text = "Complex path ![alt](/path/to/image.png)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('alt', '/path/to/image.png')])

    def test_extract_images_empty(self):
        text = "No images here, just text"
        result = extract_markdown_images(text)
        self.assertEqual(result, [])

    def test_extract_images_with_urls(self):
        text = "Image with URL ![alt](https://example.com/image.jpg)"
        result = extract_markdown_images(text)
        self.assertEqual(result, [('alt', 'https://example.com/image.jpg')])

    def test_extract_links_basic(self):
        text = "Here's a [link](http://example.com)"
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link', 'http://example.com')])

    def test_extract_links_multiple(self):
        text = """
        First [link1](http://example1.com)
        Second [link2](http://example2.com)
        """
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link1', 'http://example1.com'),
                                  ('link2', 'http://example2.com')])

    def test_extract_links_with_images(self):
        text = """
        This is a ![image](img.jpg) and this is a [link](example.com)
        """
        result = extract_markdown_links(text)
        self.assertEqual(result, [('link', 'example.com')])

    def test_extract_links_empty(self):
        text = "No links here, just text"
        result = extract_markdown_links(text)
        self.assertEqual(result, [])

    def test_extract_links_complex(self):
        text = """
        Here's a [link with spaces](https://example.com/path/to/page)
        And an ![image](img.jpg) followed by another [link](doc.pdf)
        """
        result = extract_markdown_links(text)
        self.assertEqual(result, [
            ('link with spaces', 'https://example.com/path/to/page'),
            ('link', 'doc.pdf')
        ])


if __name__ == '__main__':
    unittest.main()
