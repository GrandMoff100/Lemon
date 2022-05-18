from lemon import Table, render

data = Table(
    [
        ["Name", "Location", "Status"],
        ["Ted", "New York", "Busy"],
        ["Angie", "France", "Free"],
    ]
)

print(render(data))
