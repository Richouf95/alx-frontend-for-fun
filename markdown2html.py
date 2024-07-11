#!/usr/bin/python3
"""
From markdown to html
"""
import sys
import os
import re
import hashlib


def convert_heading(line):
    """
    Convert a Markdown heading to HTML heading
    """
    match = re.match(r'^(#{1,6}) (.+)', line)
    if match:
        heading_level = len(match.group(1))
        heading_text = match.group(2)
        return "<h{}>{}</h{}>\n".format(heading_level,
                                        heading_text,
                                        heading_level)
    return None


def convert_unordered_list(lines, index):
    """
    Convert Markdown unordered list to HTML list
    """
    html_lines = []
    while index < len(lines) and re.match(r'^- (.+)', lines[index]):
        match = re.match(r'^- (.+)', lines[index])
        if match:
            item_text = match.group(1)
            item_text = apply_transformations(item_text)
            html_lines.append("<li>{}</li>".format(item_text))
        index += 1

    if html_lines:
        return "<ul>\n" + "\n".join(html_lines) + "\n</ul>\n", index
    return None, index


def convert_ordered_list(lines, index):
    """
    Convert Markdown ordered list to HTML list
    """
    html_lines = []
    while index < len(lines) and re.match(r'^\* (.+)', lines[index]):
        match = re.match(r'^\* (.+)', lines[index])
        if match:
            item_text = match.group(1)
            item_text = apply_transformations(item_text)
            html_lines.append("<li>{}</li>".format(item_text))
        index += 1

    if html_lines:
        return "<ol>\n" + "\n".join(html_lines) + "\n</ol>\n", index
    return None, index


def convert_paragraph(line):
    """
    Convert a Markdown paragraph to HTML paragraph
    """
    if line.strip():  
        html_line = "<p>\n{}\n</p>\n".format(line.strip())
        return html_line
    return ""


def apply_transformations(line):
    """
    Apply transformations for [[text]] to MD5 and ((text)) to remove 'c'
    """
    # Check for [[text]] and apply MD5 transformation
    line = re.sub(
        r'\[\[(.*?)\]\]',
        lambda match: hashlib.md5(match.group(1).encode('utf-8')).hexdigest(),
        line)

    # Check for ((text)) and remove 'c' (case insensitive)
    line = re.sub(
        r'\(\((.*?)\)\)',
        lambda match: match.group(1).replace('c', '').replace('C', ''),
        line)

    # Check for **text** and convert to <b>text</b>
    line = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', line)

    # Check for __text__ and convert to <i>text</i>
    line = re.sub(r'__(.*?)__', r'<em>\1</em>', line)

    return line


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
            index = 0
            while index < len(lines):
                line = lines[index].strip()
                html_line = convert_heading(line)
                if html_line:
                    html_file.write(html_line)
                else:
                    html_line, index = convert_unordered_list(lines, index)
                    if html_line:
                        html_file.write(html_line)
                    else:
                        html_line, index = convert_ordered_list(lines, index)
                        if html_line:
                            html_file.write(html_line)
                        else:
                            # If it's neither heading nor list,
                            # check for transformations
                            html_line = convert_paragraph(line)
                            html_line = apply_transformations(html_line)
                            html_file.write(html_line)
                index += 1

    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)


if __name__ == "__main__":
    markdown_to_html()
