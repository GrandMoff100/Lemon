from lemon import Header, dumps, loads


document = [
    Header("My Awesome Project"),
    "This project is so awesome that you should go star it on GitHub!",
    Header("Description"),
    "You can implement nested sub-headers like magic!",
]


print(content := dumps(document))

print(loads(content))
