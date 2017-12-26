
import requests
from errorRes import ErrorResponse
import os
import csv
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from compareProperties import CompareProperty

login_url = 'https://www.fundthatflip.com/users/sign_in'
username = 'ellie.nickson123@gmail.com'
psword = 'Crowd1234566$$$'

session = requests.session()
pageURL = 'https://www.fundthatflip.com/deals?page='
baseURL = 'https://www.fundthatflip.com/deals'
progress = []
fund = []

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


def login():
    global username, psword, session, login_url
    print "get started logging in"
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, 'html.parser')
    token = soup.select('.new_session > input')[1]['value']
    token_utf8 = soup.select('.new_session > input')[0]['value']
    # print token
    # print token_utf8
    param = {
        "user[email]": username,
        "user[password]": psword,
        "authenticity_token": token,
        'utf8': token_utf8,
        'user[remember_me]': '0',
        'commit': 'Login'
    }

    ua = UserAgent()
    user_agent = ua.random

    header = {
        "User-Agent": user_agent
    }

    session.post(login_url, headers=header, data=param)

    res = session.get('https://www.fundthatflip.com/deals/10353', headers=header, data=param)
    if res.status_code == 200:
        print "login successfully"
        # print res.text
    else:
        raise ErrorResponse("login failed, error code %s" % res.status_code)


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

    filename = folder + '/' + name

    with open(filename, 'wb') as pdfwriter:
        pdfwriter.write(content)
