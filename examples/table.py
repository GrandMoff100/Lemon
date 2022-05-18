from lemon import Table, dumps

data = Table(
    [
        ["Name", "Location", "Status"],
        ["Ted", "New York", "Busy"],
        ["Angie", "France", "Free"],
    ]
)

print(dumps(data))
