import Global_Para as gp
from FileReaderWriter import FileReaderWriter
from Parser import Parser
from More_Op import more_Op as mo

from bs4 import BeautifulSoup
import logging
import sys

class ParseFundedPro():

    __config = ""
    __soup = ""
    __crawl_data = []

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("get started to crawl funded properties")
        self.__config = FileReaderWriter.readFundedConfig()
        properties_list = self.__soup.select(self.__config["funded_list"]["param"])
        for each_property in properties_list:
            one_property = {}
            for variable_name in self.__config.keys():
                if variable_name == "funded_list":
                    continue

                config = self.__config[variable_name]
                if variable_name == "variables":
                    one_property.update(Parser.parseKeyValue(each_property, config))
                elif isinstance(config, unicode) and config in mo.keys():
                    one_property.update(Parser.parseStringVariable(config, variable_name))
                elif isinstance(config, unicode) and config not in mo.keys():
                    one_property.update({variable_name: config})
                else:
                    if "replacement" in config:
                        one_property.update(Parser.parseSpecificVariable(each_property, config, variable_name, replacement=config["replacement"]))
                    else:
                        one_property.update(Parser.parseSpecificVariable(each_property, config, variable_name))
            # print one_property
            self.__crawl_data.append(one_property)
        return self.__crawl_data


