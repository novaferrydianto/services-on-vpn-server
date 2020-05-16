import json

class JsonObject(object):
    def __init__(self, data):
        self.__dict__ = json.loads(data)
