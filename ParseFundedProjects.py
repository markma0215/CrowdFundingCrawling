import Global_Para as gp
from FileReaderWriter import FileReaderWriter
from Parser import Parser
from More_Op import more_Op as mo

from bs4 import BeautifulSoup
import logging
from IsSame import checkSame

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
            one_property = self.__compare(one_property)
            self.__crawl_data.append(one_property)
        return self.__crawl_data

    def __compare(self, property):
        key = property["Campaign Name"] + property["Fund Name"]
        if key in gp.funded_data:
            oldOne = gp.funded_data[key]
            property.update({"First_Time(0/1)": 0})
            property.update({"Campaign ID": oldOne["Campaign ID"]})
            if checkSame.IsSame(oldOne, property):
                print "Campaign %s and ID %s do not have any change" % (property["Campaign Name"], property["Campaign ID"])
                return checkSame.eraseSameVariables(property)
            else:
                print "Campaign %s and ID %s do have changes" % (
                property["Campaign Name"], property["Campaign ID"])
                return checkSame.getChangedVariables(oldOne, property)
        elif key in gp.progress_data:
            property.update({"First_Time(0/1)": 1})
            property.update({"Campaign ID": str(gp.funded_campaign_id + 1)})
            print "Campaign %s comes from progress properties" % property["Campaign Name"]
            return property
        else:
            property.update({"First_Time(0/1)": 1})
            property.update({"Campaign ID": str(gp.funded_campaign_id + 1)})
            print "Campaign %s air drops into the funded groups"
            return property

