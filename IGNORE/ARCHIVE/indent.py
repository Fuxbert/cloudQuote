import textwrap

text = "This is a long string that should wrap and indent properly across multiple lines."

indent = "  "  # Two spaces
width = 30
adjusted_width = width - len(indent)

wrapped = textwrap.fill(
    text,
    width=adjusted_width,
    initial_indent=indent,
    subsequent_indent=indent
)

print(wrapped)