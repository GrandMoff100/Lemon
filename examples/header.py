from lemon import Header, render

document = Header(
    "My Awesome Project",
    [
        "This project is so awesome that you should go star it on GitHub!",
        Header(
            "Description",
            "You can implement nested sub-headers like magic!"
        )
    ]
)


print(render(document))