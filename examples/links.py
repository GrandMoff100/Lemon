from lemon import Link, dumps, loads

link = Link(
    Link(
        "",
        "https://example.com/foobars-are-tasty.png",
        media=True,
    ),
    "https://somewebsite.com/",
)


print(content := dumps(link))
# [![](https://example.com/foobars-are-tasty.png)](https://somewebsite.com/)
# Makes an image a link!

print(loads(content))
# [
#   Link(
#       Link(
#           '',
#           'https://example.com/foobars-are-tasty.png',
#           media=True,
#           title=None
#       ),
#       'https://somewebsite.com/',
#       media=False,
#       title=None
#   )
# ]
