from parent_node import ParentNode
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
    quote = r'^> .*\n( *> .*\n)*'
    unordered_list = r'(?:(?:^|\n)[*-]\s+.*(?:\n|$))+'
    ordered_list = r'(?:(?:^|\n)\d+\. +.*(?:\n|$))+'

    if re.match(heading, markdown):
        return "heading"
    elif re.match(code, markdown):
        return "code"
    elif re.match(quote, markdown.lstrip()):
        return "quote"
    elif re.match(unordered_list, markdown):
        return "unordered_list"
    elif re.match(ordered_list, markdown):
        return "ordered_list"
    elif (markdown.startswith(">")):
        return "quote"
    else:
        return "paragraph"


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    children = []
    for block in blocks:
        if block == "":
            continue
        html_node = ""
        type = block_to_block_type(block)
        match type:
            case "heading":
                html_node = heading_to_html_node(block)
                children.append(html_node)
            case "code":
                html_node = code_to_html(block)
                children.append(html_node)
            case "quote":
                html_node = quote_to_html(block)
                children.append(html_node)
            case "unordered_list":
                html_node = ul_to_html(block)
                children.append(html_node)
            case "ordered_list":
                html_node = ol_to_html(block)
                children.append(html_node)
            case "paragraph":
                html_node = paragraph_to_html(block)
                children.append(html_node)
    return ParentNode("div", children)


def text_to_children(text):
    t_nodes = text_to_textnodes(text)
    children = []
    for text_node in t_nodes:
        html = text_node.text_node_to_html_node()
        children.append(html)
    return children


def heading_to_html_node(block):
    level = 0
    for character in block:
        if character == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError("invalid heading")
    text = block[level + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html(block):
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def quote_to_html(block):
    divided = block.split("\n")
    lines = []
    for item in divided:

        if not item.startswith(">"):
            raise ValueError("invalid quote")
        # print(f"formatted: {item.lstrip(" > ").strip()}")
        lines.append(item.lstrip("> ").strip())
    quote = " ".join(lines)
    children = text_to_children(quote)
    return ParentNode("blockquote", children)


def ul_to_html(block):
    list_items = block.split("\n")
    html = []
    for item in list_items:
        text = item[2:]
        children = text_to_children(text)
        html.append(ParentNode("li", children))
    return ParentNode("ul", html)


def ol_to_html(block):
    list_items = block.split("\n")
    html = []
    for item in list_items:
        text = item[2:]
        children = text_to_children(text.strip())
        html.append(ParentNode("li", children))
    return ParentNode("ol", html)


def paragraph_to_html(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def extract_title(md):
    h1_pattern = r"^# .*$"  # Regex to match H1 headings
    match = re.search(h1_pattern, md, flags=re.MULTILINE)
    if match:
        return match.group(0).strip('# ').rstrip()
    else:
        raise Exception("No h1 found")
