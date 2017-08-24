
import Global_Para as gp
from ParseFundedProjects import ParseFundedPro as Funded
from ParseCurrentProjects import ParseCurrentPro as Current
import sys
import requests
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

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
    # sessionid, properties = login()
    # gp.login_cookies[sessionid["name"]] = sessionid["value"]
    #
    # result = requests.session().get(properties, cookies = gp.login_cookies)
    # html_text = result.text         # get "https://app.crowdstreet.com/properties/" html page

    # fundedPro = Funded(html_text)
    # currentPro = Current(html_text)
    #
    # fundedPro.parse()

    login()
    response = gp.session.get("https://app.crowdstreet.com/properties/chase-suites-overland-park/")
    print response.status_code

if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logging.info("Get Started to Crawl")
    main()

