import Global_Para as gp

import urllib2
from bs4 import BeautifulSoup
import logging
import time

class ParseFundedPro():

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')
        self.__dataFrame = []
        self.__variables = {

        }

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        fundedBlocks = self.__soup.find_all("div", class_ = "row closed-property-list")
        if len(fundedBlocks) != 1:
            logging.error("the length of funded block is not 1, it is %s" % len(fundedBlocks))
            logging.error(gp.website_structure_has_changed)
            return

        all_funded = fundedBlocks[0].find_all("div", class_ = "col-md-4 col-sm-6")
        if len(all_funded) == 0:
            logging.warn("the number of funded projects are 0")
            return

        for child in all_funded:
            pass

