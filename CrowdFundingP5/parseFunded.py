import global_param as gp
from bs4 import BeautifulSoup
import datetime
from parser import Parser


class ParseFunded(Parser):
    fundPro = []
    allData = []
    result = []

    def __init__(self):
        self.fundPro = gp.fund

    def parser(self):
        index = 1
        for item in self.fundPro:
            print 'parsing funded NO. %d' % index
            self.parseOne(item)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('fund')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'fund')

        return self.allData, self.fieldname, self.result

    def parseOne(self, item):

        data = self.getData(item)

        link = gp.baseURL + item.select_one('.deal-details > a')['href'].replace('/deals', '')
        html = gp.session.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        data.update(self.getLocation(soup))
        data.update(self.refreshBasic(data['Campaign Name'], data['Location']))

        if gp.firstCollect or data['First_Time(0/1)'] is '1':
            data.update(self.getInsideData(soup))
            self.saveHTMLpage(html=html.text.encode('utf-8', 'replace'), name=data['Campaign Name'] + '_fund',
                              compID=data['Campaign ID'])
            self.savePDFS(soup, 'fund', data['Campaign ID'])

        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'fund'))
        else:
            self.allData.append(data)

    def getID(self, name_loation):
        if gp.firstCollect:
            gp.compID += 1
            return str(gp.compID)

        prevID = gp.comparePro.getID(name_loation, 'fund')
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
            'Campaign ID': ' ',
            'Campaign Name': self.getName(item),
            'Portal ID': '5',
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': ' ',
            'Funded(0/1)': '1',
            '% Funded': '100',
            'Date Posted': ' ',
            'Date Funded': ' '
        }

    def isFirstTime(self, name):
        if gp.firstCollect:
            return '0'

        if gp.comparePro.getID(name, 'fund') == -1:
            return '1'
        else:
            return '0'

    def refreshBasic(self, name, location):
        return {
            'Campaign ID': self.getID(name + location),
            'First_Time(0/1)': self.isFirstTime(name + location)
        }
