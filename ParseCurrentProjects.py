import Global_Para as gp

import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import logging
from FileReaderWriter import FileReaderWriter


class ParseCurrentPro():

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        config = FileReaderWriter.readConfig()["current"]
        print config

    def downloadPDF(self, property_url):
        response_home_page = gp.session.get(property_url)
        if response_home_page.status_code == 200:
            home_page_soup = BeautifulSoup(response_home_page.text, "html.parser")
        else:
            print response_home_page.status_code
            print "in confirmPDF function, code is not right"
            sys.exit(1)

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
