
import Global_Para as gp
from ParseFundedProjects import ParseFundedPro as Funded
from ParseCurrentProjects import ParseCurrentPro as Current

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import os
import requests
import logging
import copy


def readystate_complete(d):
    return d.execute_script("return document.readyState") == "complete"

# first of all, login the website, get cookies
def login():
    ChromeDriver = webdriver.Chrome(os.getcwd() + "/chromedriver")
    ChromeDriver.get(gp.login_url)
    user = ChromeDriver.find_element_by_id("id_email")
    user.send_keys(gp.username)
    password = ChromeDriver.find_element_by_id("id_password")
    password.send_keys(gp.password)
    connect = ChromeDriver.find_element_by_id("id_login_submit")
    connect.click()
    WebDriverWait(ChromeDriver, 30).until(readystate_complete)
    current_url = ChromeDriver.current_url
    cookie = ChromeDriver.get_cookie("sessionid")
    ChromeDriver.close()
    return cookie, current_url


def main():
    sessionid, properties = login()
    gp.login_cookies[sessionid["name"]] = sessionid["value"]

    result = requests.session().get(properties, cookies = gp.login_cookies)
    html_text = result.text         # get "https://app.crowdstreet.com/properties/" html page

    fundedPro = Funded(html_text)
    currentPro = Current(html_text)

    fundedPro.parse()



if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logging.info("Get Started to Crawl")
    main()

