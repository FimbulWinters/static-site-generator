from textnode import *

def main():
    node = TextNode("This is a text node", TextType.Bold, "https://www.boot.dev")
    print(node.__repr__())

main()