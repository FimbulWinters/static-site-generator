from textnode import TextNode, TextType
import re

# old nodes is a list


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
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
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
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

    print("beans!!!!!!!!!")

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
                new_nodes.append(TextNode(sections[i], TextType.IMAGES, url))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if not node.text:
            continue

        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        if not links:
            new_nodes.append(node)
            continue

        sections = re.split(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", node.text)

        for i in range(len(sections)):
            if not sections[i]:  # Skip empty strings
                continue
            if i % 3 == 0:
                new_nodes.append(TextNode(sections[i], TextType.TEXT))
            elif i % 3 == 1:
                url = sections[i + 1]
                new_nodes.append(TextNode(sections[i], TextType.LINKS, url))

    return new_nodes


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        stripped_blocks.append(block)
    return stripped_blocks


def block_to_block_type(markdown):
    heading = r'^(#{1,6})\s+(.+?)(?:\s+#*)?$'
    code = r'```.*?```'
    quote = r'(?:^>.*$\n?)+'
    unordered_list = r'(?:(?:^|\n)[*-]\s+.*(?:\n|$))+'
    ordered_list = r'(?:(?:^|\n)\d+\. +.*(?:\n|$))+'

    if re.match(heading, markdown):
        return "heading"
    elif re.match(code, markdown):
        return "code"
    elif re.match(quote, markdown):
        return "quote"
    elif re.match(unordered_list, markdown):
        return "unordered_list"
    elif re.match(ordered_list, markdown):
        return "ordered_list"
    else:
        return "paragraph"
