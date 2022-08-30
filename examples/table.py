from lemon import Table, dumps, loads

data = Table(
    [
        ["Ted", "New York", "Busy"],
        ["Angie", "France", "Free"],
    ],
    ["Name", "Location", "Status"],
)

print(content := dumps(data))

print(loads(content))
