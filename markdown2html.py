#!/usr/bin/python3
"""
From markdown to html
"""
import sys
import os
import re

def convert_heading(line):
    """
    Convert a Markdown heading to HTML heading
    """
    match = re.match(r'^(#{1,6}) (.+)', line)
    if match:
        heading_level = len(match.group(1))
        heading_text = match.group(2)
        return "<h{}>{}</h{}>\n".format(heading_level, heading_text, heading_level)
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
            html_lines.append("<li>{}</li>".format(item_text))
        index += 1

    if html_lines:
        return "<ol>\n" + "\n".join(html_lines) + "\n</ol>\n", index
    return None, index

def convert_paragraph(lines, index):
    """
    Convert consecutive lines of text into a single HTML paragraph
    """
    html_lines = []
    while index < len(lines) and lines[index].strip():
        html_lines.append(lines[index].strip())
        index += 1

    if html_lines:
        html_paragraph = "<p>\n{}\n</p>\n".format("<br/>\n".join(html_lines))
        return html_paragraph, index
    return None, index

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
                            html_line, index = convert_paragraph(lines, index)
                            if html_line:
                                html_file.write(html_line)
                            else:
                                # If it's none of the above, write the original line to HTML
                                html_file.write(line + '\n')
                index += 1

    except Exception as e:
        sys.stderr.write("Error: {}\n".format(e))
        sys.exit(1)

if __name__ == "__main__":
    markdown_to_html()
