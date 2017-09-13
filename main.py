
import Global_Para as gp
from ParseFundedProjects import ParseFundedPro as Funded
from ParseCurrentProjects import ParseCurrentPro as Current
import sys
import requests
import logging
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from FileReaderWriter import FileReaderWriter as FRW



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


def getFundedProcessNameList(funded, process):

    funded_namelist = []
    process_namelist = []
    for each_property in funded:
        funded_namelist = funded_namelist + each_property.keys()

    # for each_property in process:
    #     process_namelist = process_namelist + each_property.keys()

    funded_namelist = gp.funded_variables_anchors + sorted(list(set(funded_namelist) - set(gp.funded_variables_anchors)))
    # process_namelist = gp.in_process_variables_anchors + sorted(list(set(process_namelist) - set(gp.in_process_variables_anchors)))
    print funded_namelist
    return funded_namelist, process_namelist


def main():
    login()
    all_property_page = gp.session.get("https://app.crowdstreet.com/properties/")

    # current = Current(all_property_page.text)
    # in_process_properties = current.parse()

    funded = Funded(all_property_page.text)
    funded_properties = funded.parse()

    funded, process = getFundedProcessNameList(funded_properties, gp.in_process_variables)



if __name__ == "__main__":


    input = raw_input("Is first time to crawl this website? Yes: 1, No: 0\n")
    if input == "1":
        gp.isFirstTime = True
    elif input == "0":
        gp.isFirstTime = False
        funded_variable_names, funded_data = FRW.readRunFundedProperties()
        progress_variable_names, progress_data = FRW.readInProgressProperties()
    else:
        print "please enter 1 for yes, 0 for no."
        print "Because wrong input, the system exits"
        sys.exit(1)

    logging.basicConfig(level=logging.INFO)
    logging.info("Get Started to Crawl")
    main()




