import json


class FileReaderWriter():
    @classmethod
    def readConfig(cls):
        config_file = open("config.json", "r")
        config_dict = json.load(config_file)
        return config_dict
