import Global_Para as gp
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
from FileReaderWriter import FileReaderWriter
from Parser import Parser
import os.path


class ParseCurrentPro():
    __config = ""
    __soup = ""
    __crawl_data = []
    __learn_more_response = ""

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        logging.info("get started to crawl current properties")
        self.__config = FileReaderWriter.readCurrentConfig()
        current_list_json = self.__config["current_list"]
        current_list = self.__soup.select(current_list_json["param"])
        for each_property in current_list:
            one_property = self.__parse_normal_variables(each_property, self.__config["link"], "link")
            for each_variable in self.__config:
                if each_variable == "current_list":
                    continue
                if each_variable == "Learn More":
                    one_property.update(self.__parse_learn_more(link=one_property["link"]))
                else:
                    config = self.__config[each_variable]
                    one_property.update(self.__parse_normal_variables(each_property, config, each_variable))
            self.__saveHTML(one_property)
            print one_property
            self.__crawl_data.append(one_property)

        return self.__crawl_data

    def __parse_normal_variables(self, element, config, variable_name):
        one_property = {}
        if isinstance(config, unicode) and len(config) <= 1:
            one_property.update({variable_name: config})
        elif isinstance(config, unicode) and "_withElement" in config:
            config = config.replace("_withElement", "").strip()
            one_property.update(Parser.parseStringWithEle(element, config, variable_name))
        elif isinstance(config, unicode) and len(config) > 1:
            one_property.update(Parser.parseStringVariable(config, variable_name))
        else:
            one_property.update(Parser.parseSpecificVariable(element, config, variable_name))

        return one_property

    def __parse_learn_more(self, link):
        if not link:
            return
        learn_more_link = gp.base_url + link
        html_page = gp.session.get(learn_more_link)
        if html_page.status_code is not 200:
            print "get learn more page error"
            print "code is %s" % html_page.status_code
            sys.exit(1)
        self.__learn_more_response = html_page
        element = BeautifulSoup(html_page.text, "html.parser")
        learn_more_config = self.__config["Learn More"]
        one_property = {}
        for each_variable in learn_more_config.keys():
            config = learn_more_config[each_variable]
            if not isinstance(config, dict):
                one_property.update(self.__parse_normal_variables(element, config, each_variable))
            else:
                one_property.update(Parser.parseKeyValue(element, config))

        return one_property

    def __saveHTML(self, one_property):
        file_name = gp.Documents_In_Progress.replace("{ID}", one_property["Campaign ID"])
        if not os.path.exists(file_name):
            os.makedirs(file_name)
        file_name = file_name + "/" + one_property["Campaign Name"] + ".html"
        with open(file_name, "w") as fd:
            fd.write(self.__learn_more_response.text.encode("utf-8"))


    def downloadPDF(self, property_url):

        home_page_soup = BeautifulSoup(self.__learn_more_response.text, "html.parser")
        param = {
            "request-access-terms-agreement": "true"
        }
        param_list = home_page_soup.select(".form-horizontal > input")
        for each_param in param_list:
            key = each_param["name"]
            value = each_param["value"]
            param.update({key: value})

        ua = UserAgent()
        user_agent = ua.random
        header = {
            "User-Agent": user_agent
        }

        response = gp.session.post(
            "https://app.crowdstreet.com/properties/bv-multifamily-fund/confidentiality-agreement/",
            headers=header, data=param)
        print response.status_code
        # ".no-left-margin .list-unstyled > li > a"

