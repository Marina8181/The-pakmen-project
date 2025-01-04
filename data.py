import json
def load(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data
