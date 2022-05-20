from lemon import CodeSnippet, InlineCode, Markdown, dumps, loads

document = Markdown(
    "The most telling sign of a python beginner is the use of",
    InlineCode("range(len(obj))"),
    "vs",
    InlineCode("enumerate(obj)"),
    ".",
)

print(content := dumps(document))
# The most telling sign of a python beginner is the use of ``range(len(obj))`` vs ``enumerate(obj)`` .

print(loads(content))
# [Markdown('The most telling sign of a python beginner is the use of', InlineCode('range(len(obj))'), 'vs', InlineCode('enumerate(obj)'), '.')]

snippet = CodeSnippet(
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
