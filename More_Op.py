
import Global_Para as gp
import datetime


def string(element):
    return element.string


def href_attribute(element):
    return element['href']


def current_campaign_id():
    gp.current_campaign_id = gp.current_campaign_id + 1
    return gp.current_campaign_id


def collection_date():
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d")


def isFirstTime():
    if gp.isFirstTime:
        return 1
    else:
        return 0


def hasVideoPitch(element):
    video_pitch = element.find("div", class_="wistia_video_foam_dummy")
    if video_pitch:
        return True
    else:
        return False


def extractBusinessPlan(element):
    summaries = element.select(".summary-table-container .col-lg-12")
    business_plan = ""
    for each_summary in summaries:
        if each_summary.h3 and each_summary.h3.string == "The Business Plan":
            each_summary.find("ul", class_="nav nav-tabs").decompose()
            for each_string in each_summary.stripped_strings:
                each_string = each_string.strip("\n").strip()
                if each_string == "The Business Plan":
                    continue
                business_plan = business_plan + each_string.replace("*", "").replace("/", " ").strip() + " "
            break

    return business_plan.strip()


def saveHTMLpage(response):
    with open("c_page.html", "w") as fd:
        fd.write(response.text.encode("utf-8"))


more_Op = {
    "string": string,
    "href_attribute": href_attribute,
    "current_campaign_id": current_campaign_id,
    "collection_date": collection_date,
    "isFirstTime": isFirstTime,
    "hasVideoPitch": hasVideoPitch,
    "extractBusinessPlan": extractBusinessPlan,
    "saveHTMLpage": saveHTMLpage
}