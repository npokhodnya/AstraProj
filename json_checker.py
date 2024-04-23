import json


def get_data():
    with open("./config.json", encoding="utf-8", mode="r") as read_file:
        data = json.load(read_file)

    return data
