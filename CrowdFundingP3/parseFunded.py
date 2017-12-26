import global_param as gp
from bs4 import BeautifulSoup
from errorRes import ErrorResponse
import datetime


class ParseFunded:
    threePart = []
    allData = []
    fieldname = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date', 'First_Time(0/1)', 'Funded(0/1)',
                 'Date Posted', 'Date Funded', '% Funded', 'Type']
    result = []
    num = 1

    def __init__(self):
        html = gp.session.get(gp.past_invest)
        soup = BeautifulSoup(html.text, 'html.parser')
        self.threePart = soup.select('.io-browse')
        if len(self.threePart) != 3:
            raise ErrorResponse('in past invest, content error')

    def parser(self):
        for i in range(len(self.threePart)):
            self.parseOne(i)

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('fund')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'fund')

        return self.allData, self.fieldname, self.result

    def parseOne(self, index):

        while self.threePart[index].select_one('.item-list > ul > li > a') is not None:
            items = self.threePart[index].select('.view-content .io-browse__property-item')
            for item in items:
                print 'collecting number %d data' % self.num
                data = self.getData(item)
                if not gp.firstCollect:
                    self.result.append(gp.comparePro.detectChanges(data, 'fund'))
                else:
                    self.allData.append(data)
                self.num += 1

            link = gp.baseURL + self.threePart[index].select_one('.item-list > ul > li > a')['href']
            html = gp.session.get(link)
            soup = BeautifulSoup(html.text, 'html.parser')
            self.threePart[index] = soup.select('.io-browse')[index]

        items = self.threePart[index].select('.view-content .io-browse__property-item')
        for item in items:
            data = self.getData(item)
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

    def getType(self, item):
        type = item.select_one('.rm-header').string.encode('utf-8')
        return type.strip('\r\n').strip()

    def getName(self, item):
        name = item.select_one('.io-browse__property-title .field-content').string.encode('utf-8')
        return name.strip('\r\n').strip()

    def getData(self, item):
        data = self.getBasicData(item)
        data.update(self.getOtherData(item))
        return data

    def getBasicData(self, item):
        return {
            'Campaign ID': self.getID(self.getName(item)),
            'Type': self.getType(item),
            'Campaign Name': self.getName(item),
            'Portal ID': '3',
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': self.isFirstTime(self.getName(item)),
            'Funded(0/1)': '1',
            '% Funded': '100',
            'Date Posted': ' ',
            'Date Funded': ' '
        }

    def getOtherData(self, item):
        labels = item.select('.io-browse__property-field-label')
        values = item.select('.io-browse__property-field-value')

        otherData = {}
        for i in range(len(labels)):
            try:
                label = gp.toString(labels[i])
            except:
                continue

            try:
                value = gp.toString(values[i])
            except:
                value = ' '

            if label not in self.fieldname:  # append field name in excel
                self.fieldname.append(label)

            otherData.update({label: value})

        return otherData

    def isFirstTime(self, name):
        if gp.firstCollect:
            return '0'

        if gp.comparePro.getID(name, 'fund') == -1:
            return '1'
        else:
            return '0'
