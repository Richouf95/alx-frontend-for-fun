#!/usr/bin/python3
"""
From markdown to html
"""
import sys
import os


def markdown_to_html():
    """
    Transform markdown file to html
    """
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html")
        sys.exit(1)

    markdown_file_name = sys.argv[1]
    html_file_name = sys.argv[2]

    if not os.path.exists(markdown_file_name):
        print("Missing <filename>")
        sys.exit(1)

    print("arg 1 : {}".format(markdown_file_name))
    print("arg 2 : {}".format(html_file_name))

if __name__ == "__main__":
    markdown_to_html()
