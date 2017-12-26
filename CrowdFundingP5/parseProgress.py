
import global_param as gp
from bs4 import BeautifulSoup
import datetime
from parser import Parser


class ParseProgress(Parser):
    processPro = []
    compID = 0
    allData = []
    result = []

    def __init__(self):
        self.processPro = gp.progress

    def parse(self):
        index = 1
        for item in self.processPro:
            print 'parsing in process NO. %d' % index
            self.parseNormalOne(item)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('process')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'process')

        return self.allData, self.fieldname, self.result

    def parseNormalOne(self, item):
        data = self.getData(item)

        link = gp.baseURL + item.select_one('.deal-details > a')['href'].replace('/deals', '')
        html = gp.session.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        data.update(self.getLocation(soup))
        data.update(self.refreshBasic(data['Campaign Name'], data['Location']))

        if gp.firstCollect or data['First_Time(0/1)'] is '1':
            data.update(self.getFundedAmount(soup))
            data.update(self.getInsideData(soup))
            self.saveHTMLpage(html=html.text.encode('utf-8', 'replace'), name=data['Campaign Name'] + '_process',
                              compID=data['Campaign ID'])
            self.savePDFS(soup, 'process', data['Campaign ID'])

        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'process'))
        else:
            self.allData.append(data)

    def getID(self, name_location):

        if gp.firstCollect:
            gp.compID += 1
            return str(gp.compID)

        prevID = gp.comparePro.getID(name_location, 'process')
        if prevID == -1:
            gp.compID += 1
            return str(gp.compID)
        else:
            return str(prevID)

    def getData(self, item):
        data = self.getBasicData(item)
        return data

    def getBasicData(self, item):
        return {
            'Portal ID': '5',
            'Campaign Name': self.getName(item),
            'Campaign ID': ' ',
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': ' ',
            'Funded(0/1)': '0',
            '% Funded': self.getFundedPercentage(item),
            'Date Posted': ' ',
            'Date Funded': ' '
        }

    def getFundedAmount(self, soup):
        fund = soup.select_one('.text-center > span')
        if 'Funded Amount' not in self.fieldname:
            self.fieldname.append('Funded Amount')

        return {
            'Funded Amount': fund.string.strip('\r\n').strip().encode('utf-8')
        }

    def getFundedPercentage(self, soup):
        percentage = soup.select_one('.progress-bar')
        if percentage is None:
            return ' '

        percentage = percentage.string.strip('\r\n').strip().encode('utf-8').replace(' ', '').replace('Funded!', '')
        return percentage

    def isFirstTime(self, name):
        if gp.firstCollect:
            return '0'

        if gp.comparePro.getID(name, 'process') == -1:
            return '1'
        else:
            return '0'

    def refreshBasic(self, name, location):
        return {
            'Campaign ID': self.getID(name + location),
            'First_Time(0/1)': self.isFirstTime(name + location)
        }