
import requests
from errorRes import ErrorResponse
import os
import csv
from compareProperties import CompareProperty
from fake_useragent import UserAgent

login_url = 'https://www.realcrowd.com/securityapi/login'
username = 'ellie.nickson123@gmail.com'
psword = 'Crowd1234566$$$'

session = requests.session()
past_invest = 'https://www.realcrowd.com/past-offerings'
oppen_invest = 'https://www.realcrowd.com/offerings'
baseURL = 'https://www.realcrowd.com'

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

    param = {
        "userName": username,
        "password": psword
    }

    ua = UserAgent()
    user_agent = ua.random
    # print "the fake user agent is %s " % user_agent
    header = {
        "User-Agent": user_agent
    }

    session.post(login_url, headers=header, data=param)

    res = session.get('https://www.realcrowd.com/offerings/j-and-r-investments/adams-building-historic-renovation-in-tulsa')
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

    filename = folder + '/' + name.replace('/', '_')

    with open(filename, 'wb') as pdfwriter:
        pdfwriter.write(content)
