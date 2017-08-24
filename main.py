
import Global_Para as gp
from ParseFundedProjects import ParseFundedPro as Funded
from ParseCurrentProjects import ParseCurrentPro as Current
import sys
import requests
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import json

def login():
    logging.info("get started to login")
    session = requests.session()
    login_page = session.get(gp.login_url)
    if login_page.status_code == 200:
        login_soup = BeautifulSoup(login_page.text, "html.parser")
    else:
        print "cannot get login page, the error code is %s " % login_page.status_code
        sys.exit(1)

    token = login_soup.find("form", id="login-form").contents[1]['value']
    param = {
        "email": gp.username,
        "password": gp.password,
        "csrfmiddlewaretoken": token
    }

    ua = UserAgent()
    user_agent = ua.random
    print "the fake user agent is %s " % user_agent
    header = {
        "User-Agent": user_agent
    }

    session.post(gp.login_url, headers=header, data=param)
    gp.session = session
    logging.info("finished login process")


def main():
    login()
    response = gp.session.get("https://app.crowdstreet.com/properties/brookview-village/")
    print response.status_code
    soup = BeautifulSoup(response.text, "html.parser")
    # element = soup.find("div", class_="col-sm-12 col-md-6 col-lg-4")
    label = soup.select_one(".summary-items .summary-table > tbody > tr > td + td")
    print label
    # print len(names)

    # config_file = open("config.json", "r")
    # config_dict = json.load(config_file)
    # print config_dict.keys()

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logging.info("Get Started to Crawl")
    main()

