
import bs4
import global_param as gp
from errorRes import ErrorResponse


class Parser(object):

    # subVariables = {
    #     'Asset Profile':
    # }

    def __init__(self):
        self.fieldname = [
            'Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date', 'First_Time(0/1)', 'Funded(0/1)',
            'Date Posted', 'Date Funded', '% Funded', 'Location']
        super(Parser, self).__init__()

    def getName(self, item):
        curPro = item.select_one('.card-title').string.strip('\r\n').strip().encode('utf-8')
        return curPro

    def getCompanyName(self, item):
        compName = item.select_one('.rc-sponsor-name').string.strip('\r\n').replace('By ', '').strip().encode('utf-8', 'replace')
        if 'Company Name' not in self.fieldname:
            self.fieldname.append('Company Name')
        return {
            'Company Name': compName
        }

    def getSponsorType(self, item):
        sType = item.select_one('.rc-sponsor-category').string.strip('\r\n').replace('Sponsor', '').strip().encode('utf-8', 'replace')
        if 'Sponsor Type' not in self.fieldname:
            self.fieldname.append('Sponsor Type')
        return {
            'Sponsor Type': sType
        }

    def getLocation(self, item):
        location = item.select_one('.rc-location-caption').string.strip('\r\n').strip().encode('utf-8', 'replace')
        if 'Location' not in self.fieldname:
            self.fieldname.append('Location')
        return {
            'Location': location
        }

    def getPropertyType(self, item):
        pType = item.select_one('.text-truncate > span').string.strip('\r\n').strip().encode('utf-8', 'replace')
        if 'Property Type' not in self.fieldname:
            self.fieldname.append('Property Type')
        return {
            'Property Type': pType
        }

    def getInvestmentType(self, item):
        if 'Investment Type' not in self.fieldname:
            self.fieldname.append('Investment Type')
        return {
            'Investment Type': ' '
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

    def saveHTMLpage(self, html, name, compID):
        gp.writeDocument('documents', name + '.html', html, compID)

    def savePDFsHelper(self, pdf, name, compID):
        gp.writeDocument('documents', name + '.pdf', pdf, compID)

    def savePDFS(self, soup, category, compID):
        document = [section for section in soup.select('.rc-offering-documents > tbody > tr > td > a') if section.string is not None]

        if not document:
            return

        for eachLink in document:
            pdf = gp.session.get(gp.baseURL + eachLink['href'])
            self.savePDFsHelper(pdf.content, eachLink.string.strip('\r\n').strip() + '_' + category, compID)

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