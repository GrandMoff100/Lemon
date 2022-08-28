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

print(loads(content))
