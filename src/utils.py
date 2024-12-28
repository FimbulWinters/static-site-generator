from textnode import TextNode, TextType
import re

# old nodes is a list


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.Text:
            new_nodes.append(node)
            continue
        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.Text))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not node.text:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        if not images:
            new_nodes.append(node)
            continue

        sections = re.split(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

        for i in range(len(sections)):
            if not sections[i]:  # Skip empty strings
                continue
            if i % 3 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            elif i % 3 == 1:
                url = sections[i + 1]
                new_nodes.append(TextNode(sections[i], TextType.IMAGE, url))

    return new_nodes


# def split_nodes_link(old_nodes):
