import Global_Para as gp
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
from FileReaderWriter import FileReaderWriter
from Parser import Parser
import os.path
from IsSame import checkSame


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

            hasBefore, one_property = self.__compare(one_property)
            if not hasBefore:
                print "Campaign %s is a new guy" % one_property["Campaign Name"]
                self.__saveHTML(one_property)
                self.__downloadPDF(one_property)

            del one_property["link"]
            self.__crawl_data.append(one_property)

        return self.__crawl_data

    def __compare(self, property):
        """Compare the new in progress properties with old ones"""
        key = property["Campaign Name"] + property["Fund Name"]
        if key in gp.progress_data:
            oldOne = gp.progress_data[key]
            property.update({"First_Time(0/1)": 0})
            property.update({"Campaign ID": oldOne["Campaign ID"]})
            if checkSame.IsSame(oldOne, property):
                property = checkSame.eraseSameVariables(property)
                print "Campaign %s and ID is %s do not have changes" % (property["Campaign Name"], property["Campaign ID"])
                return False, property
            else:
                print "Campaign %s and ID is %s do have changes" % (
                property["Campaign Name"], property["Campaign ID"])
                return False, checkSame.getChangedVariables(oldOne, property)
        else:
            property.update({"First_Time(0/1)": 1})
            property.update({"Campaign ID": (gp.current_campaign_id + 1)})
            return True, property

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

    def __downloadPDF(self, one_property):
        home_page_soup = BeautifulSoup(self.__learn_more_response.text, "html.parser")
        pdf_links = home_page_soup.select(".no-left-margin .list-unstyled > li > a")
        for each_link in pdf_links:
            link = each_link["href"]
            if "confidentiality-agreement" in link:
                print "Campaign ID: %s has agreement" % one_property["Campaign ID"]
                self.__aggre_confidentiality(link, home_page_soup)
                document_link = each_link["data-document-url"]
                pdf_url = gp.base_url + document_link
                pdf_name = each_link.span.string.strip()
            else:
                print "Campaign ID: %s does not have agreement" % one_property["Campaign ID"]
                pdf_url = gp.base_url + link
                pdf_name = each_link.string.strip()
            response = gp.session.get(pdf_url)
            if response.status_code != 200:
                print "in download PDF, response code is not 200"
                print response.status_code
                sys.exit(1)
            file_name = gp.Documents_In_Progress.replace("{ID}", one_property["Campaign ID"]) + "/" + pdf_name + ".pdf"
            with open(file_name, "wb") as pdfwriter:
                pdfwriter.write(response.content)

    def __aggre_confidentiality(self, link, soup):
        param = {
            "request-access-terms-agreement": "true"
        }
        param_list = soup.select(".form-horizontal > input")
        for each_param in param_list:
            key = each_param["name"]
            value = each_param["value"]
            param.update({key: value})

        ua = UserAgent()
        user_agent = ua.random
        header = {
            "User-Agent": user_agent
        }

        agreement_link = gp.base_url + link
        response = gp.session.post(agreement_link, headers=header, data=param)
        if response.status_code != 200:
            print "in agreement response, code is not 200"
            print response.status_code
            sys.exit(1)



