import json


def serialize(path, data: dict):
    """

    :param path: path to config.json
    :param data: dict of settings
    :return: None
    """
    with open(path, 'w') as f:
        try:
            json.dump(data, f)
            print(f"Serialized data: {data}")
        except Exception as e:
            print(e)


def deserialize(path) -> dict:
    """

    :param path: path to config.json
    :return: list of deserialized data from config.json
    """
    with open(path, 'r') as f:
        data = json.load(f)

    return data
