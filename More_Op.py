
import Global_Para as gp
import datetime
import sys


def string(element):
    content = element.string
    if content:
        return content.strip('\n').strip()
    else:
        return ""


def href_attribute(element):
    return element['href']


def current_campaign_id():
    gp.current_campaign_id = gp.current_campaign_id + 1
    return str(gp.current_campaign_id)


def collection_date():
    now = datetime.datetime.now()
    now = now.strftime("%Y-%m-%d")
    return now


def isFirstTime():
    if gp.isFirstTime:
        return 1
    else:
        return 0


def hasVideoPitch(element):
    video_pitch = element.find("div", class_="wistia_responsive_wrapper")
    if video_pitch:
        return "1"
    else:
        return "0"


def extractBusinessPlan(element):
    summaries = element.find_all("div", class_="row summary-table-container")
    business_plan = ""
    for each_summary in summaries:
        title = each_summary.select_one(".col-lg-12 > h3")
        if title and title.string and "Business Plan" in title.string.strip():
            if each_summary.find("ul", class_="nav nav-tabs"):
                each_summary.find("ul", class_="nav nav-tabs").decompose()
            for each_string in each_summary.stripped_strings:
                each_string = each_string.strip("\n").strip()
                if each_string == "The Business Plan" or each_string == "Business Plan":
                    continue
                business_plan = business_plan + each_string.replace("*", "").replace("/", " ").strip() + " "
            break

    return business_plan.strip()


more_Op = {
    "string": string,
    "href_attribute": href_attribute,
    "current_campaign_id": current_campaign_id,
    "collection_date": collection_date,
    "isFirstTime": isFirstTime,
    "hasVideoPitch": hasVideoPitch,
    "extractBusinessPlan": extractBusinessPlan
}