import global_param as gp
from bs4 import BeautifulSoup
import datetime
from parser import Parser


class ParseFunded(Parser):
    fundPro = []
    allData = []
    result = []

    def __init__(self):
        html = gp.session.get(gp.past_invest)
        soup = BeautifulSoup(html.text, 'html.parser')
        allCurrent = soup.select_one('.justify-content-center')
        self.fundPro = [oneProperty for oneProperty in allCurrent.select('.col-12')]
        super(ParseFunded, self).__init__()

    def parser(self):
        index = 1
        for item in self.fundPro:
            print 'parsing funded NO. %d' % index
            self.parseOne(item)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('fund')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'fund')

        # print self.fieldname
        return self.allData, self.fieldname, self.result

    def parseOne(self, item):

        data = self.getOutSideData(item)

        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'fund'))
        else:
            self.allData.append(data)

    def getID(self, name):
        if gp.firstCollect:
            gp.compID += 1
            return str(gp.compID)

        prevID = gp.comparePro.getID(name, 'fund')
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
        data.update(self.getFundedAmount(item))

        return data

    def getBasicData(self, item):
        return {
            'Campaign ID': self.getID(self.getName(item)),
            'Campaign Name': self.getName(item),
            'Portal ID': '7',
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': self.isFirstTime(self.getName(item)),
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

    def getFundedAmount(self, item):
        if 'Funding Amount' not in self.fieldname:
            self.fieldname.append('Funding Amount')

        amount = item.select_one('.rc-closed-state > strong').string.strip('\r\n').strip().encode('utf-8')
        if amount != 'Fully Funded':
            amount = amount.split()[-1]

        return {
            'Funding Amount': amount
        }