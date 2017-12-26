
import global_param as gp
from bs4 import BeautifulSoup
from errorRes import ErrorResponse
import bs4
import datetime


class ParseProgress:
    fiveParts = []
    fieldname = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date', 'First_Time(0/1)', 'Funded(0/1)',
                 'Date Posted', 'Date Funded', '% Funded', 'Type']
    compID = 0
    allData = []
    result = []
    num = 1

    def __init__(self):
        html = gp.session.get(gp.oppen_invest)
        soup = BeautifulSoup(html.text, 'html.parser')
        self.fiveParts = soup.select('.io-browse')
        if len(self.fiveParts) != 5:
            print 'in progress projects, there is no 5 parts'
            answer = raw_input('continue to collect data? yes, no\n')
            if answer != 'yes':
                raise ErrorResponse('in progress collecting process, abort!')

    def parse(self):
        for i in range(len(self.fiveParts)):
            self.parseNormalOne(i)

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('process')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'process')

        return self.allData, self.fieldname, self.result

    def parseNormalOne(self, index):

        compType = self.getType(self.fiveParts[index])
        if compType == 'Open to All Investors':
            return

        items = self.fiveParts[index].select('.io-browse__property-item')
        for item in items:
            if 'placeholder' in item['class']:
                continue

            print 'collecting number %d data' % self.num

            data = {'Type': compType}
            data.update(self.getDataOutside(item))

            if item.select_one('.io_browse_details-button > a') is None:
                if not gp.firstCollect:
                    self.result.append(gp.comparePro.detectChanges(data, 'process'))
                else:
                    self.allData.append(data)
                continue
            self.num += 1

            link = gp.oppen_invest + item.select_one('.io_browse_details-button > a')['href'].replace('/node', '')
            # print link
            html = gp.session.get(link)
            # print html.text
            soup = BeautifulSoup(html.text, 'html.parser')
            data.update(self.getInsideData(soup))

            if not gp.firstCollect:
                self.result.append(gp.comparePro.detectChanges(data, 'process'))
            else:
                self.allData.append(data)

            if data['First_Time(0/1)'] == '1' or gp.firstCollect:
                self.saveHTMLpage(html.text.encode('utf-8', 'replace'), data['Campaign Name'], data['Campaign ID'])

                # save PDF files
                pdfTags = soup.select('.io-equity-content-top-btns__files')
                pdfFiles = []
                for each in pdfTags:
                    pdfFiles += each.find_all('a')

                for pdftag in pdfFiles:
                    link = pdftag['href']
                    name = pdftag.string.encode('utf-8').strip('\r\n').strip()
                    pdfText = gp.session.get(link).content
                    self.savePDFs(pdfText, name, data['Campaign ID'])

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

    def getType(self, onePart):
        type = onePart.select_one('.io-browse__investment-status-title').string.encode('utf-8')
        return type.strip('\r\n').strip()

    def getName(self, item):
        name = item.select_one('.io-browse__property-title, .rm-analytics-processed').string.encode('utf-8').strip('\r\n').strip()
        return name

    def getDataOutside(self, item):
        data = self.getBasicData(item)
        data.update(self.getOtherData(item, '.io-browse__property-field-label', '.io-browse__property-field-value'))
        return data

    def getBasicData(self, item):
        return {
            'Portal ID': '3',
            'Campaign Name': self.getName(item),
            'Campaign ID': self.getID(self.getName(item)),
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': self.isFirstTime(self.getName(item)),
            'Funded(0/1)': '0',
            '% Funded': ' ',
            'Date Posted': ' ',
            'Date Funded': ' ',
            'Funded': ' ',
            'Expected': ' '
        }

    def getOtherData(self, item, cssPathLabel, cssPathValue):
        otherData = {}
        labels = item.select(cssPathLabel)
        values = item.select(cssPathValue)

        if len(values) == 12:
            del values[7]

        for i in range(len(labels)):
            try:
                label = gp.toString(labels[i])
            except:
                continue

            try:
                value = gp.toString(values[i])
            except:
                value = ' '

            if label not in self.fieldname:
                self.fieldname.append(label)

            otherData.update({label: value})

        return otherData

    def getInsideData(self, soup):
        data = {}
        data.update(self.getFundedAmount(soup))
        data.update(self.getOtherData(soup, '.io-equity-overview__label', '.io-equity-overview__value'))
        data.update(self.getOtherData(soup, '.io-equity-sideblock__row_label', '.io-equity-sideblock__row_value'))

        # print '; '.join(str(key) + '=' + str(value) for key, value in data.items())
        business = soup.select_one('.io-equity-investment-main .io-equity-main__section-content .field-content')

        if 'Business Plan' not in self.fieldname:
            self.fieldname.append('Business Plan')

        if not business:
            data.update({'Business Plan': ' '})
            return data

        allTags = [child for child in business.descendants if child.name == 'p' or child.name == 'li']

        allText = []
        for eachTag in allTags:
            for descendant in eachTag.descendants:
                if isinstance(descendant, bs4.element.NavigableString) and descendant.string is not None:
                    allText.append(descendant.string)

        text = "".join(t.strip('\r\n') for t in allText)
        text = text.replace('\r\n', '').replace(u'\xa0', ' ').strip()
        if len(text) > 32200:
            text = text[:32200]
            text = text[:text.rfind(' ')]

        text = ' '.join(t for t in text.split())
        text = text.encode('utf-8', 'replace')
        data.update({'Business Plan': text})


        return data

    def getFundedAmount(self, soup):
        if 'Funded' not in self.fieldname:
            self.fieldname.append('Funded')

        if 'Expected' not in self.fieldname:
            self.fieldname.append('Expected')

        amount = soup.select_one('.funded-amount')
        if amount is None:
            return {
                'Funded': ' ',
                'Expected': ' '
            }

        amount = amount.string.encode('utf-8').strip('\r\n').strip()
        if 'Fully Funded' in amount:
            amount = amount.replace('Fully Funded', '').strip()
            return {
                'Funded': amount.encode('utf-8'),
                'Expected': amount.encode('utf-8')
            }
        elif 'Amount TBA' == amount:
            return {
                'Funded': 'Amount TBA'.encode('utf-8'),
                'Expected': 'Amount TBA'.encode('utf-8')
            }
        else:
            return{
                'Funded': amount.split()[0].encode('utf-8'),
                'Expected': amount.split()[2].encode('utf-8')
            }

    def saveHTMLpage(self, html, name, compID):
        gp.writeDocument('documents', name + '.html', html, compID)

    def savePDFs(self, pdf, name, compID):
        gp.writeDocument('documents', name + '.pdf', pdf, compID)

    def isFirstTime(self, name):
        if gp.firstCollect:
            return 0

        if gp.comparePro.getID(name, 'process') == -1:
            return '1'
        else:
            return '0'