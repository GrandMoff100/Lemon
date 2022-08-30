from lemon import CodeBlock, InlineCode, Text, dumps, loads

document = Text(
    "The most telling sign of a python beginner is the use of",
    InlineCode("range(len(obj))"),
    "vs",
    InlineCode("enumerate(obj)"),
)

print(content := dumps(document))

print(loads(content))

snippet = CodeBlock(
    """
import python

def topsecretcode():
    print("Hello World")

foobar()
""",
    "python",
)


print(content := dumps(snippet))

# ```python
# import python
#
# def topsecretcode():
#     print("Hello World")
#
# foobar()
# ```

print(loads(content))
