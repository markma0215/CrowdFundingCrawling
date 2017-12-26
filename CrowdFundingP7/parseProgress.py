
import global_param as gp
from bs4 import BeautifulSoup
import datetime
from parser import Parser
import bs4


class ParseProgress(Parser):
    processPro = []
    compID = 0
    allData = []
    result = []

    def __init__(self):
        html = gp.session.get(gp.oppen_invest)
        soup = BeautifulSoup(html.text, 'html.parser')
        allCurrent = soup.find(id='currentlyfundraising-section')
        self.processPro = [oneProperty for oneProperty in allCurrent.select('.col-12')]
        super(ParseProgress, self).__init__()

    def parse(self):
        index = 1
        for item in self.processPro:
            print 'parsing in process NO. %d' % index
            self.parseOne(item)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('process')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'process')

        return self.allData, self.fieldname, self.result

    def parseOne(self, item):
        data = self.getOutSideData(item)
        link = gp.oppen_invest + item.select_one('.btn-success')['href'].replace('/offerings', '')
        html = gp.session.get(link)
        soup = BeautifulSoup(html.text, 'html.parser')
        data.update(self.getInsideData(soup))

        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'process'))
            if data['First_Time(0/1)'] == '1':
                print 'save pdf'
                self.saveHTMLpage(html=html.text.encode('utf-8', 'replace'), name=data['Campaign Name'] + '_process', compID=data['Campaign ID'])
                self.savePDFS(soup, 'process', data['Campaign ID'])
        else:
            self.allData.append(data)
            self.saveHTMLpage(html=html.text.encode('utf-8', 'replace'), name=data['Campaign Name'] + '_process', compID=data['Campaign ID'])
            self.savePDFS(soup, 'process', data['Campaign ID'])

    def getID(self, name):

        if gp.firstCollect:
            gp.compID += 1
            return str(gp.compID)

        prevID = gp.comparePro.getID(name, 'process')
        if prevID == -1:
            gp.compID += 1
            return str(gp.compID)
        else:
            return str(prevID)

    def getOutSideData(self, item):
        data = self.getBasicData(item)
        data.update(self.getCompanyName(item))
        data.update(self.getSponsorType(item))
        data.update(self.getLocation(item))
        data.update(self.getPropertyType(item))
        data.update(self.getInvestmentType(item))
        data.update(self.getOneDimenData(item, '.rc-stat-title', '.rc-stat-value'))

        return data

    def getBasicData(self, item):
        return {
            'Portal ID': '7',
            'Campaign Name': self.getName(item),
            'Campaign ID': self.getID(self.getName(item)),
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': self.isFirstTime(self.getName(item)),
            'Funded(0/1)': '0',
            '% Funded': ' ',
            'Date Posted': ' ',
            'Date Funded': ' '
        }

    def getInsideData(self, item):

        data = {}
        data.update(self.getOneDimenData(item, '.d-none > div > div > dl > dd > span',
                                         '.d-none > div > div > dl > dt'))

        description = []
        desTag = item.select_one('.col-sm-6 .mb-3')
        description.append(self.toString(desTag.div, False))
        desTag = item.select_one('.col-sm-6 > ul')
        description.append(self.toString(desTag, False))
        description = ' '.join(description)

        data.update({
            'About this fund': description
        })
        if 'About this fund' not in self.fieldname:
            self.fieldname.append('About this fund')

        return data

    def isFirstTime(self, name):
        if gp.firstCollect:
            return '0'

        if gp.comparePro.getID(name, 'process') == -1:
            return '1'
        else:
            return '0'