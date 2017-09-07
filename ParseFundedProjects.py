import Global_Para as gp

from bs4 import BeautifulSoup
import logging

class ParseFundedPro():

    def __init__(self, html_page):
        self.__soup = BeautifulSoup(html_page, 'html.parser')

    def parse(self):
        logging.basicConfig(level=logging.INFO)


