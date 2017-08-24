import Global_Para as gp

import urllib2
from bs4 import BeautifulSoup
import logging


class ParseCurrentPro():

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')

    def parse(self):
        logging.basicConfig(level=logging.INFO)
        currentBlock = self.__soup.find_all("div", class_="row active-property-list")
        if len(currentBlock) != 1:
            logging.error("the length of current block is not 1, it is %s" % len(currentBlock))
            logging.error(gp.website_structure_has_changed)
            return

    #https://app.crowdstreet.com/accounts/login/


