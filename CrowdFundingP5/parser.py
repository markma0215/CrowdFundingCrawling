
from errorRes import ErrorResponse
import global_param as gp


class Parser:

    oneDimen = ['Investment Summary', 'About the Property']
    twoDimen = ['Use of Proceeds', 'Loan to Cost', 'Valuation']
    fieldname = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date', 'First_Time(0/1)', 'Funded(0/1)',
                 'Date Posted', 'Date Funded', '% Funded', 'Location']

    def getName(self, item):
        name = item.select_one('.deal-details > a > h4').string.encode('utf-8').strip('\r\n').strip()
        return name

    def getOneDimenData(self, item, cssPathLabel, cssPathValue):
        labels = item.select(cssPathLabel)
        values = item.select(cssPathValue)

        otherData = {}
        for i in range(len(labels)):
            try:
                label = labels[i].string.strip('\r\n').strip().encode('utf-8')
            except:
                continue

            try:
                value = values[i].string.strip('\r\n').strip().encode('utf-8')
            except:
                value = ' '

            if label not in self.fieldname:  # append field name in excel
                self.fieldname.append(label)

            otherData.update({label: value})

        return otherData

    def getTwoDimenData(self, item, rowCssPath, columnCssPath, dataCssPath):
        rowNames = []
        for one in item.select(rowCssPath):
            if one.string is None:
                rowNames.append(one.contents[0].string.strip('\r\n').strip())
            else:
                rowNames.append(one.string.strip('\r\n').strip())

        columnNames = [one.string.strip('\r\n').strip() for one in item.thead.find_all('th')
                       if one.string.replace('&nbsp', '').strip('\r\n').strip()
                       and one.string.replace('&nbsp', '').strip('\r\n').strip() != 'Valuation Method']

        data = item.select(dataCssPath)

        if len(data) != (len(rowNames) * len(columnNames)):
            raise ErrorResponse('in two dimension table, the number of data does not match row * column'
                                ' Data length is %d, row length is %d and column length is %d' % (len(data), len(rowNames), len(columnNames)))

        otherData = {}

        for i in range(len(rowNames)):
            for j in range(len(columnNames)):
                label = rowNames[i].encode('utf-8') + "_" + columnNames[j].encode('utf-8')
                value = data[i * len(columnNames) + j].string.strip('\r\n').strip().encode('utf-8')

                if label not in self.fieldname:
                    self.fieldname.append(label)

                otherData.update({label: value})

        return otherData

    def getLocation(self, soup):
        location = soup.select_one('.deal-main-content .visible-lg')
        location = [l for l in location.contents if l != '\n']
        data = {'Location': location[1].string.encode('utf-8').strip('\r\n').strip()}
        return data

    def getInsideData(self, soup):
        data = {}
        data.update(self.getOneDimenData(soup, '.list-item .key', '.list-item .value'))        # up right table
        data.update(self.getOneDimenData(soup, '.text-center .pad0', '.text-center > td'))     # up right table header

        deal_sections = soup.select('.deal-info')
        for oneDeal in deal_sections:
            if oneDeal.h3.string.strip('\r\n').strip() in self.oneDimen:                    # invest, about
                data.update(self.getOneDimenData(oneDeal, '.table-bordered > tbody > tr > th', '.table-bordered > tbody > tr > td'))
            elif oneDeal.h3.string.strip('\r\n').strip() in self.twoDimen:
                data.update(self.getTwoDimenData(oneDeal, rowCssPath='.table-bordered > tbody > tr > th',
                                                 columnCssPath='.table-bordered > thead > tr > th',
                                                 dataCssPath='.table-bordered > tbody > tr > td'))
        return data

    def saveHTMLpage(self, html, name, compID):
        gp.writeDocument('documents', name + '.html', html, compID)

    def savePDFsHelper(self, pdf, name, compID):
        gp.writeDocument('documents', name + '.pdf', pdf, compID)

    def savePDFS(self, soup, category, compID):
        document = [section for section in soup.select('.deal-info') if section.h3.string == 'Documents']
        if not document:
            return

        links = [link for link in document[0].select('p > a')]
        for eachLink in links:
            pdf = gp.session.get(eachLink['href'])
            self.savePDFsHelper(pdf.content, eachLink.contents[1].string.strip('\r\n').strip() + '_' + category, compID)