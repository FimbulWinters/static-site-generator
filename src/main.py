import shutil
from textnode import *
import os


def copy_static(source, dest, count):
    if count == 0:
        shutil.rmtree(dest)
        count += 1

    print(f"source: {source}")
    print(f"dest: {dest}")
    if not os.path.exists(dest):
        print("no")
        os.mkdir(dest)

    print(f"dir lest: {os.listdir(source)}")

    for item in os.listdir(source):
        print(f"item: {item}")
        source_path = os.path.join(source, item)
        print(f"src path: {source_path}")
        dest_path = os.path.join(dest, item)
        print(f"dest path: {dest_path}")
        if os.path.isfile(source_path):
            shutil.copy(source_path, dest_path)
        else:
            copy_static(source_path, dest_path, count)


def main():
    node = TextNode("This is a text node", TextType.BOLD,
                    "https://www.boot.dev")
    copy_static('./static', './public', 0)


main()
