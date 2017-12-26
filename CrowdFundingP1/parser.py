# -*- coding: utf-8 -*-

from errorRes import ErrorResponse
import bs4

class Parser(object):

    def __init__(self):
        super(Parser, self).__init__()
        self.fieldname = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date', 'First_Time(0/1)', 'Funded(0/1)',
            'Date Posted', 'Date Funded', '% Funded', 'Location']

    def getName(self, item):
        name = item.select_one('.theme__title___3qCP3')
        name = self.toString(name)
        return name

    def getLocation(self, item, category):
        node = item.select_one('.theme__subtitle___3p3mO')
        if category == 'fund':
            if 'Funding Amount' not in self.fieldname:
                self.fieldname.append('Funding Amount')

            if 'Num. Investors' not in self.fieldname:
                self.fieldname.append('Num. Investors')

            if node is None:
                return {
                    'Funding Amount': '',
                    'Num. Investors': '',
                    'Location': ''
                }
            else:
                return {
                    'Funding Amount': node.string.split(' • '.decode('utf-8'))[0].encode('utf-8').strip('\r\n').strip(),
                    'Num. Investors': node.string.split(' • '.decode('utf-8'))[1].encode('utf-8').strip('\r\n').strip(),
                    'Location': ''
                }

        else:
            if node is None:
                return {
                    'Location': ''
                }
            else:
                return {
                    'Location': node.string.strip('\r\n').strip().encode('utf-8')
                }

    def getFundName(self, item):
        node = item.select_one('.KHYeL')
        node = self.toString(node)
        if 'Fund Name' not in self.fieldname:
            self.fieldname.append('Fund Name')
        return {
            'Fund Name': node
        }

    def getComment(self, item):
        coms = item.select('.theme__chip___3Iv9P')
        if 'Comment (seasoned/repeated etc.)' not in self.fieldname:
            self.fieldname.append('Comment (seasoned/repeated etc.)')

        if coms is None:
            return {
                'Comment (seasoned/repeated etc.)': ''
            }

        comsValue = []
        for oneCom in coms:
            comsValue.append(self.toString(oneCom))

        return {
            'Comment (seasoned/repeated etc.)': ' '.join(comsValue)
        }

    def getOneDimenData(self, item, labelCsspath, valueCsspath, *arg):
        labels = item.select(labelCsspath)
        values = item.select(valueCsspath)

        otherData = {}
        for i in range(len(labels)):
            try:
                label = self.toString(labels[i])
                if arg and label in arg:
                    continue
            except:
                continue

            try:
                value = self.toString(values[i])
            except:
                value = ' '

            if label not in self.fieldname:
                self.fieldname.append(label)

            otherData.update({label: value})

        return otherData

    def toString(self, item, isFirst=True):
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
