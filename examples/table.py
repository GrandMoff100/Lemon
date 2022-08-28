from lemon import Table, dumps, loads

data = Table(
    [
        ["Name", "Location", "Status"],
        ["Ted", "New York", "Busy"],
        ["Angie", "France", "Free"],
    ]
)

print(content := dumps(data))

print(loads(content))
