from lemon import Header, dumps, loads

document = Header(
    "My Awesome Project",
    [
        "This project is so awesome that you should go star it on GitHub!",
        Header("Description", "You can implement nested sub-headers like magic!"),
    ],
)


print(content := dumps(document))
"""
# My Awesome Project

This project is so awesome that you should go star it on GitHub!

## Description

You can implement nested sub-headers like magic!
"""

print(loads(content))
"""
[
    Header(
        'My Awesome Project',
        [5
            'This project is so awesome that you should go star it on GitHub!',
            Header(
                'Description',
                ['You can implement nested sub-headers like magic!']
            )
        ]
    )
]
"""
