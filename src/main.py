import shutil
from textnode import *
import os

from utils import extract_title, markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    print(
        f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path)
    contents = file.read()

    template_file = open(template_path)
    template_contents = template_file.read()

    md_contents = markdown_to_html_node(contents)
    html = md_contents.to_html()

    title = extract_title(contents)

    template_amended = template_contents.replace(
        "Title", title).replace("Content", html).replace("{", "").replace("}", "")

    print(template_amended)
    if os.path.exists(dest_path):
        os.remove(dest_path)
        replacement = open(dest_path, 'x')
        replacement.write(template_amended)
        replacement.close()
    else:
        created = open(dest_path, 'x')
        created.write(template_amended)
        created.close()

    file.close()
    template_file.close()


def copy_static(source, dest, count):
    if count == 0 and os.path.exists(dest):
        shutil.rmtree(dest)
        count += 1

    if not os.path.exists(dest):
        print("no")
        os.mkdir(dest)

    for item in os.listdir(source):
        source_path = os.path.join(source, item)
        dest_path = os.path.join(dest, item)
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_static(source_path, dest_path, count)


def main():
    node = TextNode("This is a text node", TextType.BOLD,
                    "https://www.boot.dev")

    if os.path.exists('./public'):
        shutil.rmtree('./public')

    copy_static('./static', './public', 0)

    generate_page('./content/index.md', './template.html',
                  './public/index.html')


main()
