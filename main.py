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


def getMaximumCampaignID(data):
    compaign_max = 0
    for each_property in data:
        compaign_id = int(each_property["Campaign ID"])
        if compaign_max < compaign_id:
            compaign_max = compaign_id
    return compaign_max


def buildPreviousModel(data):
    model = {}
    for each_data in data:
        key = each_data["Campaign Name"] + each_data["Fund Name"]
        value = each_data
        model.update({key: value})
    return model


def buildAfterCrawlingModel(data):
    model = {}
    for each_data in data:
        key = each_data["Campaign ID"] + ", " + each_data["Campaign Name"]
        model.update({key: None})
    return model


def compareBeforewithAfter(in_progress_prev=None, in_progress_next=None,
                           funded_prev=None, funded_next=None):
    continue_in_progress = []
    convert_to_funded = []
    in_progress_disappeared = []

    continue_in_funded = []
    funded_disappeared = []
    for each_property in in_progress_prev:
        if each_property in in_progress_next:
            continue_in_progress.append(each_property)
        elif each_property in funded_next:
            convert_to_funded.append(each_property)
        else:
            in_progress_disappeared.append(each_property)

    for each_property in funded_prev:
        if each_property in funded_next:
            continue_in_funded.append(each_property)
        else:
            funded_disappeared.append(each_property)

    continue_in_progress = " ".join(x for x in continue_in_progress)
    convert_to_funded = " ".join(x for x in convert_to_funded)
    in_progress_disappeared = " ".join(x for x in in_progress_disappeared)
    continue_in_funded = " ".join(x for x in continue_in_funded)
    funded_disappeared = " ".join(x for x in funded_disappeared)

    logging.info("Results:")
    logging.info("Properties that keep living in the progress are %s " % continue_in_progress)
    logging.info("Properties that jump to the funded group are %s " % convert_to_funded)
    logging.info("Properties that disappeared while in progress before are %s " % in_progress_disappeared)
    logging.info("Properties that keep living in the funded group are %s " % continue_in_funded)
    logging.info("Properties that disappeared while in funded group before are %s " % funded_disappeared)


def getFundedProcessNameList(funded, process):
    funded_namelist = []
    process_namelist = []
    for each_property in funded:
        funded_namelist = funded_namelist + each_property.keys()

    for each_property in process:
        process_namelist = process_namelist + each_property.keys()

    funded_namelist = gp.funded_variables_anchors + sorted(
        list(set(funded_namelist) - set(gp.funded_variables_anchors)))
    process_namelist = gp.in_process_variables_anchors + sorted(list(set(process_namelist) - set(gp.in_process_variables_anchors)))
    print funded_namelist
    return funded_namelist, process_namelist


def main():
    gp.funded_variables_infile, gp.funded_data = FRW.readRunFundedProperties()
    gp.progress_variables_infile, gp.progress_data = FRW.readInProgressProperties()

    gp.funded_campaign_id = getMaximumCampaignID(gp.funded_data)
    gp.current_campaign_id = getMaximumCampaignID(gp.progress_data)

    funded_prev = buildAfterCrawlingModel(gp.funded_data)
    gp.funded_data = buildPreviousModel(gp.funded_data)

    in_progress_prev = buildAfterCrawlingModel(gp.progress_data)
    gp.progress_data = buildPreviousModel(gp.progress_data)


    """get stared to crawl"""
    login()
    all_property_page = gp.session.get("https://app.crowdstreet.com/properties/")

    current = Current(all_property_page.text)
    in_process_properties = current.parse()
    in_progress_next = buildAfterCrawlingModel(in_process_properties)
    logging.info("finished crawling current properties")

    funded = Funded(all_property_page.text)
    funded_properties = funded.parse()
    funded_next = buildAfterCrawlingModel(funded_properties)
    logging.info("finished crawling funded properties")

    logging.info("get started to write files")
    funded, process = getFundedProcessNameList(funded_properties, in_process_properties)
    FRW.writeRunsFundedProperties(fieldname=funded, data=funded_properties)
    FRW.writeInProgressProperties(fieldname=process, data=in_process_properties)
    logging.info("finished writing files")

    logging.info("get started to compare crawling results between previous and this one")
    compareBeforewithAfter(in_progress_prev=in_progress_prev, in_progress_next=in_progress_next,
                           funded_prev=funded_prev, funded_next=funded_next)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Get Started to Crawl")
    main()