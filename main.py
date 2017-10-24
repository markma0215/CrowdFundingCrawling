import Global_Para as gp
from ParseFundedProjects import ParseFundedPro as Funded
from ParseCurrentProjects import ParseCurrentPro as Current
import sys
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from FileReaderWriter import FileReaderWriter as FRW


def login():
    print "Get started to crawl......"
    print "Login......"
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
    # print "the fake user agent is %s " % user_agent
    header = {
        "User-Agent": user_agent
    }

    session.post(gp.login_url, headers=header, data=param)
    gp.session = session
    print "Login finished"


def getMaximumCampaignID(data):
    compaign_max = 0
    for each_property in data:
        compaign_id = int(each_property["Campaign ID"])
        if compaign_max < compaign_id:
            compaign_max = compaign_id
    return compaign_max


def buildModel(data):
    model = {}
    for each_data in data:
        key = each_data["Campaign Name"]
        value = each_data
        model.update({key: value})
    return model


def buildNameModel(data):
    model = {}
    for each_data in data:
        key = each_data["Campaign Name"]
        value = each_data
        model.update({key: value})
    return model


def compareBeforewithAfter(in_progress_prev=None, in_progress_next=None,
                           funded_prev=None, funded_next=None):
    convert_to_funded = []
    in_progress_disappeared = []

    continue_in_funded = []
    funded_disappeared = []
    for each_property in in_progress_prev:
        if each_property in funded_next:
            convert_to_funded.append(each_property)
        else:
            in_progress_disappeared.append(each_property)

    for each_property in funded_prev:
        if each_property in funded_next:
            continue_in_funded.append(each_property)
        else:
            funded_disappeared.append(each_property)

    convert_to_funded = " ".join(x for x in convert_to_funded)
    in_progress_disappeared = " ".join(x for x in in_progress_disappeared)
    continue_in_funded = " ".join(x for x in continue_in_funded)
    funded_disappeared = " ".join(x for x in funded_disappeared)

    print "Results:"
    print "Properties that jump to the funded group are %s " % convert_to_funded
    print "Properties that disappeared while in progress before are %s " % in_progress_disappeared
    print "Properties that keep living in the funded group are %s " % continue_in_funded
    print "Properties that disappeared while in funded group before are %s " % funded_disappeared


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
    # print funded_namelist
    return funded_namelist, process_namelist


def main():
    choice = raw_input("Is it the first time to COLLECT DATA? (yes / no) \n")
    if str(choice).lower() == "yes":
        gp.isFirstTime = True

    elif str(choice).lower() == "no":
        gp.isFirstTime = False
        gp.funded_variables_infile, gp.funded_data = FRW.readRunFundedProperties()
        gp.progress_variables_infile, gp.progress_data = FRW.readInProgressProperties()

        gp.funded_campaign_id = getMaximumCampaignID(gp.funded_data)
        gp.current_campaign_id = getMaximumCampaignID(gp.progress_data)

    else:
        print "please choose yes or no"
        print "system exit...."
        sys.exit(1)

    # funded_prev = buildNameModel(gp.funded_data)
    gp.funded_data = buildModel(gp.funded_data)
    #
    # in_progress_prev = buildNameModel(gp.progress_data)
    gp.progress_data = buildModel(gp.progress_data)


    """get stared to crawl"""
    login()
    all_property_page = gp.session.get("https://app.crowdstreet.com/properties/")

    current = Current(all_property_page.text)
    in_process_properties = current.parse()
    # in_progress_next = buildNameModel(in_process_properties)
    print "finished crawling current properties"

    funded = Funded(all_property_page.text)
    funded_properties = funded.parse()
    # funded_next = buildNameModel(funded_properties)
    print "finished crawling funded properties"

    print "get started to write files"
    funded, process = getFundedProcessNameList(funded_properties, in_process_properties)

    if gp.isFirstTime:
        FRW.writeFirstRunFunded(fieldname=funded, data=funded_properties)
        FRW.writeFirstRunInProgress(fieldname=process, data=in_process_properties)
    else:
        FRW.writeRunsFundedProperties(fieldname=funded, data=funded_properties)
        FRW.writeInProgressProperties(fieldname=process, data=in_process_properties)

    print "finished writing files"

    # print "get started to compare crawling results between previous and this one"
    # compareBeforewithAfter(in_progress_prev=in_progress_prev, in_progress_next=in_progress_next,
    #                        funded_prev=funded_prev, funded_next=funded_next)

if __name__ == "__main__":
    main()
