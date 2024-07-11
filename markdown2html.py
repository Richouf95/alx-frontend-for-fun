#!/usr/bin/python3
"""
From markdown to html
"""
import sys
import os
import re


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

    try:
        with open(markdown_file_name, 'r') as markdown_file:
            lines = markdown_file.readlines()

        with open(html_file_name, 'w') as html_file:
            for line in lines:
                line = line.strip()
                match = re.match(r'^(#{1,6}) (.+)', line)
                if match:
                    heading_level = len(match.group(1))
                    heading_text = match.group(2)
                    html_file.write(f"<h{heading_level}>{heading_text}</h{heading_level}>\n")

    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)


if __name__ == "__main__":
    markdown_to_html()
