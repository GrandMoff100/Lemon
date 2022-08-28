from lemon import Bold, Italics, Strikethrough, Text, dumps, loads

document = Text(
    Bold("My bold text"),
    Italics("is italisized"),
    "this is not",
    Strikethrough("and also strikethrough"),
    "and more regular text",
    Bold("But bold again"),
    Strikethrough("and then strikethrough"),
    Italics("and finally more italics."),
    "finally some regular text.",
)

print(content := dumps(document))

print(loads(content))
