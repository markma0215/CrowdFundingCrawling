
class CompareProperty:

    fundNameID = {}
    processNameID = {}

    fundIDData = {}
    processIDData = {}

    fundFieldName = []
    processFieldName = []

    prevFundData = []
    prevProcessData = []

    curFundData = []
    curProcessData = []

    notCompare = ['Data Collection Date', 'First_Time(0/1)']

    def setData(self, fundData, processData, fundField, procField):

        self.fundNameID = {fund['Campaign Name'] + fund['Location']: fund['Campaign ID'] for fund in fundData}
        self.processNameID = {process['Campaign Name'] + process['Location']: process['Campaign ID'] for process in processData}
        self.fundIDData = {fund['Campaign ID']: fund for fund in fundData}
        self.processIDData = {process['Campaign ID']: process for process in processData}
        self.fundFieldName = fundField
        self.processFieldName = procField
        self.prevFundData = fundData
        self.prevProcessData = processData

    def getNewData(self, category):
        if category == 'fund':
            return self.prevFundData + self.curFundData
        else:
            return self.prevProcessData + self.curProcessData

    def getID(self, name_location, category):
        if category == 'fund':
            if name_location in self.fundNameID:
                return self.fundNameID[name_location]
            else:
                return -1
        else:
            if name_location in self.processNameID:
                return self.processNameID[name_location]
            else:
                return -1

    def detectChanges(self, data, category):
        result = ''
        if category == 'fund':
            self.curFundData.append(data)
            if data['First_Time(0/1)'] is '1':
                result = data['Campaign ID'] + ' is a new guy!'
        else:
            if data['First_Time(0/1)'] is '1':
                result = data['Campaign ID'] + ' is a new guy!'
                self.curProcessData.append(data)
            else:
                self.curProcessData.append(data)
                for eachData in reversed(self.prevProcessData):
                    if data['Campaign ID'].strip() == eachData['Campaign ID']:
                        if data['% Funded'] != eachData['% Funded']:
                            result = data['Campaign ID'] + ' has changed the percentage of funded!'

        return result

    def detectChangesOLD(self, data, category):
        flag = False
        result = ''
        if category == 'fund':
            if data['Campaign ID'] in self.fundIDData:
                for i in range(len(self.prevFundData)):
                    if data['Campaign ID'] != self.prevFundData[i]['Campaign ID']:
                        continue
                    for eachKey in data.keys():
                        if eachKey in self.notCompare:
                            self.prevFundData[i].update({eachKey: data[eachKey]})
                            continue

                        if eachKey not in self.prevFundData[i]:
                            self.prevFundData[i].update({eachKey: data[eachKey]})
                            flag = True
                        elif data[eachKey] != self.prevFundData[i][eachKey]:
                            flag = True
                            self.prevFundData[i].update({eachKey: data[eachKey]})

                    break

            else:
                self.prevFundData.append(data)
                result = data['Campaign ID'] + ' is a new guy!'
        else:
            if data['Campaign ID'] in self.processIDData:
                for i in range(len(self.prevProcessData)):
                    if data['Campaign ID'] != self.prevProcessData[i]['Campaign ID']:
                        continue
                    for eachKey in data.keys():
                        if eachKey in self.notCompare:
                            self.prevProcessData[i].update({eachKey: data[eachKey]})
                            continue

                        if eachKey not in self.prevProcessData[i]:
                            self.prevProcessData[i].update({eachKey: data[eachKey]})
                            flag = True
                        elif data[eachKey].strip() != self.prevProcessData[i][eachKey].strip():
                            flag = True
                            self.prevProcessData[i].update({eachKey: data[eachKey]})
                    break

            else:
                self.prevProcessData.append(data)
                result = data['Campaign ID'] + ' is a new guy!'
                flag = True

        if flag:
            result = data['Campaign ID'] + ' changed info!'
        elif not result:
            result = data['Campaign ID'] + " doesn't change!"
        return result

    def combineFieldName(self, field, category):
        if 'fund' == category:
            for name in self.fundFieldName:
                if name not in field:
                    field.append(name)
        else:
            for name in self.processFieldName:
                if name not in field:
                    field.append(name)
        return field