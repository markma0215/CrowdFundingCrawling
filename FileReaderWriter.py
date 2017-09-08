import json


class FileReaderWriter():
    @classmethod
    def readCurrentConfig(cls):
        config_file = open("current_config.json", "r")
        config_dict = json.load(config_file)
        return config_dict

    @classmethod
    def readFundedConfig(cls):
        funded_file = open("funded_config.json", "r")
        funded_dict = json.load(funded_file)
        return funded_dict
