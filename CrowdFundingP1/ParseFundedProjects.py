import Global_Para as gp
from bs4 import BeautifulSoup
from compareProperties import CompareProperty
from parser import Parser
import datetime


class ParseFundedPro(Parser):

    def __init__(self):
        super(ParseFundedPro, self).__init__()
        self.fundPro = gp.fundedPro
        self.allData = []
        self.result = []

    def parser(self):
        print "get started to crawl funded properties"
        index = 1
        for eachPro in self.fundPro:
            print "collecting number %d property" % index
            self.parseOne(eachPro)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('fund')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'fund')

        return self.allData, self.fieldname, self.result

    def parseOne(self, item):
        data = self.getOutsideData(item)
        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'fund'))
        else:
            self.allData.append(data)

    def getOutsideData(self, item):
        data = self.getBasicData(item)
        data.update(self.getLocation(item, 'fund'))
        data.update(self.getFundName(item))
        data.update(self.getComment(item))
        data.update(self.getClosed(item))
        data.update(self.getOneDimenData(item, '.highlights-label', '.highlights-value'))
        return data

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

    def getBasicData(self, item):
        return {
            'Campaign ID': self.getID(self.getName(item)),
            'Campaign Name': self.getName(item),
            'Portal ID': '1',
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

    def getClosed(self, item):
        node = item.select_one('.close-date')
        node = self.toString(node, isFirst=False)
        rindex = node.rfind(' ')
        remain = node[:rindex]
        remains = remain.split()
        node = ' '.join([remains[-3], remains[-2], remains[-1]])
        if 'Closed' not in self.fieldname:
            self.fieldname.append('Closed')

        return {
            'Closed': node
        }

