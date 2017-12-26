import Global_Para as gp
import sys
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from parser import Parser
import datetime
import bs4


class ParseCurrentPro(Parser):

    def __init__(self):
        super(ParseCurrentPro, self).__init__()
        self.procePro = gp.currentPro
        self.allData = []
        self.result = []

    def parser(self):
        print "get started to crawl progress properties"
        index = 1
        for eachPro in self.procePro:
            print "collecting number %d property" % index
            self.parseOne(eachPro)
            index += 1

        if not gp.firstCollect:
            self.allData = gp.comparePro.getNewData('process')
            self.fieldname = gp.comparePro.combineFieldName(self.fieldname, 'process')

        return self.allData, self.fieldname, self.result

    def parseOne(self, item):
        data = self.getOutsideData(item)
        link = gp.base_url + self.getLink(item)
        html = gp.refreshSoup(link)
        soup = BeautifulSoup(html, 'html.parser')
        data.update(self.getInsideData(soup))

        if not gp.firstCollect:
            self.result.append(gp.comparePro.detectChanges(data, 'process'))
            if data['First_Time(0/1)'] == '1':
                print 'save pdf'
                self.saveHTMLpage(html=html.encode('utf-8', 'replace'), name=data['Campaign Name'], compID=data['Campaign ID'])
                self.savePDFS(soup, data['Campaign ID'])
        else:
            self.allData.append(data)
            self.saveHTMLpage(html=html.encode('utf-8', 'replace'), name=data['Campaign Name'],
                              compID=data['Campaign ID'])
            self.savePDFS(soup, data['Campaign ID'])

    def getInsideData(self, item):
        data = self.getOneDimenData(item, '.summary-items .summary-table > tbody > tr > td > strong',
                                    '.summary-items .summary-table > tbody > tr > td + td')
        data.update(self.getOneDimenData(item, '.summary-table > tbody > tr .key > h4',
                                         '.summary-table > tbody > tr .value'))
        if 'Video Pitch (0/1)' not in self.fieldname:
            self.fieldname.append('Video Pitch (0/1)')
        if item.find('div', class_='wistia_responsive_wrapper') is None:
            data.update({
                'Video Pitch (0/1)': '0'
            })
        else:
            data.update({
                'Video Pitch (0/1)': '1'
            })
        data.update(self.proDescription(item))
        return data

    def proDescription(self, item):

        if 'The Business Plan' not in self.fieldname:
            self.fieldname.append('The Business Plan')

        descp = ''
        allSections = item.select('.summary-table-container .col-lg-12')
        for sec in allSections:
            if sec.h3 and 'Business Plan' in sec.h3.string:
                descp = sec
                break

        if not descp:
            return {
                'The Business Plan': ''
            }

        allTags = [child for child in descp.descendants if child.name == 'p' or child.name == 'li']

        allText = []
        for eachTag in allTags:
            for descendant in eachTag.descendants:
                if isinstance(descendant, bs4.element.NavigableString) and descendant.string is not None:
                    allText.append(descendant.string)

        text = "".join(t.replace('\r\n', '').strip() for t in allText)
        if len(text) > 32200:
            text = text[:32200]
            text = text[:text.rfind(' ')]

        text = ' '.join(t for t in text.split())
        return {
            'The Business Plan': text.encode('utf-8', 'replace')
        }

    def getOutsideData(self, item):
        data = self.getBasicData(item)
        data.update(self.getLocation(item, 'process'))
        data.update(self.getFundName(item))
        data.update(self.getComment(item))
        data.update(self.getOneDimenData(item, '.highlights-label', '.highlights-value'))
        return data

    def getBasicData(self, item):
        return {
            'Campaign ID': self.getID(self.getName(item)),
            'Campaign Name': self.getName(item),
            'Portal ID': '1',
            'Data Collection Date': datetime.datetime.now().strftime("%Y-%m-%d"),
            'First_Time(0/1)': self.isFirstTime(self.getName(item)),
            'Funded(0/1)': '',
            '% Funded': '',
            'Date Posted': ' ',
            'Date Funded': ' '
        }

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

    def isFirstTime(self, name):
        if gp.firstCollect:
            return '0'

        if gp.comparePro.getID(name, 'process') == -1:
            return '1'
        else:
            return '0'

    def getLink(self, item):
        return item.select_one('.theme__title___3qCP3 > a')['href']

    def saveHTMLpage(self, html, name, compID):
        gp.writeDocument('documents', name + '.html', html, compID)

    def savePDFS(self, soup, compID):
        self.__downloadPDF(soup, compID)

    def __downloadPDF(self, item, compID):
        pdf_links = item.select(".no-left-margin .list-unstyled > li > a")
        for each_link in pdf_links:
            link = each_link["href"]
            if "confidentiality-agreement" in link:
                print "Campaign ID: %s has agreement" % compID
                self.__aggre_confidentiality(link, item)
                document_link = each_link["data-document-url"]
                pdf_url = gp.base_url + document_link
                pdf_name = each_link.span.string.strip()
            else:
                print "Campaign ID: %s does not have agreement" % compID
                pdf_url = gp.base_url + link
                pdf_name = each_link.string.strip()
            response = gp.session.get(pdf_url)
            if response.status_code != 200:
                print "in download PDF, response code is not 200"
                print response.status_code
                sys.exit(1)
            gp.writeDocument('documents', pdf_name + '.pdf', response.content, compID)

    def __aggre_confidentiality(self, link, soup):
        param = {
            "request-access-terms-agreement": "true"
        }
        param_list = soup.select(".form-horizontal > input")
        for each_param in param_list:
            key = each_param["name"]
            value = each_param["value"]
            param.update({key: value})

        ua = UserAgent()
        user_agent = ua.random
        header = {
            "User-Agent": user_agent
        }

        agreement_link = gp.base_url + link
        response = gp.session.post(agreement_link, headers=header, data=param)
        if response.status_code != 200:
            print "in agreement response, code is not 200"
            print response.status_code
            sys.exit(1)



