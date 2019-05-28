


class Lion:

    def __init__(self):
        name = "The Lion Class"

class Tiger:

    def __init__(self):
        name = "The Tiger Class"





x = "Lion"

instance = globals()[x]
print(instance.name)