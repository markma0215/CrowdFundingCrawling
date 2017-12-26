
import os
import requests
from compareProperties import CompareProperty
from errorRes import ErrorResponse
import csv
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time


# global variables
base_url = "https://app.crowdstreet.com"
login_url = "https://app.crowdstreet.com/accounts/login/"
username = "rheazhou@gmail.com"
psword = "Crowd1234566$$$"
session = requests.session()

comparePro = CompareProperty()
firstCollect = True
compID = 0
fundedPro = []
currentPro = []

outputs = {
    'documents': os.getcwd() + '/Documents_In_Progress/',
    'first_fund': os.getcwd() + '/First_Run_Funded/',
    'first_sequence': os.getcwd() + '/First_Run_In_Progress/',
    'sequence_fund': os.getcwd() + '/Subsequent_Runs_Funded/',
    'sequence_process': os.getcwd() + '/Subsequent_Runs_In_Progress/'
}


def readystate_complete(d):
    return d.execute_script("return document.readyState") == "complete"


def refreshSoup(url):
    res = session.get(url)
    if res.status_code != 200:
        raise ErrorResponse("refresh page failed, error code %s" % res.status_code)
    return res.text


def login():
    print "Get started to crawl......"
    print "Login......"
    ChromeDriver = webdriver.Chrome(os.getcwd() + "/chromedriver")
    ChromeDriver.get(login_url)

    user = ChromeDriver.find_element_by_name("email")
    user.send_keys(username)
    password = ChromeDriver.find_element_by_name('password')
    password.send_keys(psword)
    connect = ChromeDriver.find_element_by_id('id_login_submit')
    connect.click()
    WebDriverWait(ChromeDriver, 30).until(readystate_complete)
    time.sleep(10)
    cookies = ChromeDriver.get_cookies()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    html = ChromeDriver.page_source
    # print html
    ChromeDriver.close()
    print "Finished Login"
    return html


def readFile(action, name):
    global outputs
    if action not in outputs:
        raise ErrorResponse('in read file process, action is not right')

    filename = outputs[action] + name
    if not os.path.exists(filename):
        raise ErrorResponse('in read file process, file name is not right')

    with open(filename, 'rb') as csvfile:
        reader = csv.DictReader(csvfile)
        fieldname = reader.fieldnames
        prevData = [one for one in reader]

    return fieldname, prevData


def writeFile(action, name, fieldname, data):
    global outputs
    if action not in outputs:
        raise ErrorResponse('in write file process, action is not right')

    filename = outputs[action] + name
    if os.path.exists(filename):
        filename = filename + '_1.csv'

    with open(filename, 'wb') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldname, delimiter=',', lineterminator='\n')
        writer.writeheader()
        writer.writerows(data)


def writeDocument(action, name, content, compID):
    global outputs
    if action not in outputs:
        raise ErrorResponse('in write pdf file process, action is not right')

    folder = outputs[action] + str(compID)
    if not os.path.exists(folder):
        os.makedirs(folder)

    filename = folder + '/' + name.replace('/', '_')

    with open(filename, 'wb') as pdfwriter:
        pdfwriter.write(content)
