
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from errorRes import ErrorResponse
import os
import csv
from compareProperties import CompareProperty
import bs4


login_url = 'https://www.realtymogul.com/user/login'
username = 'ellie.nickson123@gmail.com'
psword = 'Crowd1234566$$$'

session = ''
past_invest = 'https://www.realtymogul.com/past-opportunities'
oppen_invest = 'https://www.realtymogul.com/investment-opportunity'
baseURL = 'https://www.realtymogul.com'

comparePro = CompareProperty()
firstCollect = True
compID = 0

outputs = {
    'documents': os.getcwd() + '/Documents_In_Progress/',
    'first_fund': os.getcwd() + '/First_Run_Funded/',
    'first_sequence': os.getcwd() + '/First_Run_In_Progress/',
    'sequence_fund': os.getcwd() + '/Subsequent_Runs_Funded/',
    'sequence_process': os.getcwd() + '/Subsequent_Runs_In_Progress/'
}


def readystate_complete(d):
     return d.execute_script("return document.readyState") == "complete"


def login():
    global username, psword, session
    print "get started logging in"
    ChromeDriver = webdriver.Chrome(os.getcwd() + "/chromedriver")
    ChromeDriver.get(login_url)

    user = ChromeDriver.find_element_by_name("name")
    user.send_keys(username)
    password = ChromeDriver.find_element_by_name('pass')
    password.send_keys(psword)
    connect = ChromeDriver.find_element_by_name('op')
    connect.click()
    WebDriverWait(ChromeDriver, 30).until(readystate_complete)
    cookies = ChromeDriver.get_cookies()
    session = requests.session()
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])
    res = session.get('https://www.realtymogul.com/investment-opportunities')
    if res.status_code == 200:
        print "login successfully"
    else:
        raise ErrorResponse("login failed, error code %s" % res.status_code)

    ChromeDriver.close()


def refreshSoup(url):
    res = session.get(url)
    if res.status_code != 200:
        raise ErrorResponse("refresh page failed, error code %s" % res.status_code)
    return res.text


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
        filename += '_1.csv'

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

    filename = folder + '/' + name

    with open(filename, 'wb') as pdfwriter:
        pdfwriter.write(content)


def toString(item, isFirst=True):
    text = []
    for each in item.descendants:
        if isinstance(each, bs4.element.NavigableString) and each.string.strip('\r\n').strip():
            if isFirst:
                return each.string.strip('\r\n').strip().encode('utf-8')
            else:
                text.append(each.string.strip('\r\n').strip().encode('utf-8'))
    if isFirst:
        raise ErrorResponse('toString method, css path is not right')
    else:
        return ' '.join(text)
