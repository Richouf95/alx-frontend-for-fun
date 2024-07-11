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
        sys.stderr.write("Usage: ./markdown2html.py README.md README.html\n")
        sys.exit(1)

    markdown_file_name = sys.argv[1]
    html_file_name = sys.argv[2]

    if not os.path.exists(markdown_file_name):
        sys.stderr.write("Missing {}\n".format(markdown_file_name))
        sys.exit(1)

    # Here you would implement the conversion from markdown to HTML
    # For now, we'll just print that the conversion would take place
    # print("arg 1 : {}".format(markdown_file_name))
    # print("arg 2 : {}".format(html_file_name))

if __name__ == "__main__":
    markdown_to_html()
