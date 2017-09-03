
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




more_Op = {
    "string": string,
    "href_attribute": href_attribute,
    "current_campaign_id": current_campaign_id,
    "collection_date": collection_date,
    "isFirstTime": isFirstTime
}