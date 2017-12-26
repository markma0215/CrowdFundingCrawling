
import global_param as gp
from parseFunded import ParseFunded
from parseProgress import ParseProgress
import sys
import traceback
import datetime

if __name__ == '__main__':

    gp.login()
    try:
        answer = raw_input('First time to collect data in this website? yes, no\n')
        if answer == 'yes':
            print 'collecting funded projects data...'
            funded = ParseFunded()
            funded_data, funded_fieldname, dummy_result = funded.parser()
            gp.writeFile(action='first_fund', name='First_Funded.csv', fieldname=funded_fieldname, data=funded_data)
            gp.writeFile(action='sequence_fund', name='First_Funded.csv', fieldname=funded_fieldname, data=funded_data)
            print 'done!'

            print 'collecting in progress projects data...'
            process = ParseProgress()
            process_data, process_fieldname, dummy_result = process.parse()
            gp.writeFile(action='first_sequence', name='First_Progress.csv', fieldname=process_fieldname, data=process_data)
            gp.writeFile(action='sequence_process', name='First_Progress.csv', fieldname=process_fieldname, data=process_data)
            print 'done!'

        elif answer == 'no':
            gp.firstCollect = False
            fund_file = raw_input('Please specify base funded file\n')
            fieldnameFUND, prevFundData = gp.readFile('sequence_fund', fund_file)

            process_file = raw_input('Please specify base process file\n')
            fieldnamePROCESS, prevProData = gp.readFile('sequence_process', process_file)

            gp.comparePro.setData(prevFundData, prevProData, fieldnameFUND, fieldnamePROCESS)
            gp.compID = len(prevFundData) + len(prevProData)

            print 'Get started to collect funded data'
            funded = ParseFunded()
            funded_data, funded_fieldname, result_fund = funded.parser()
            filename = 'Squence_Funded_' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
            gp.writeFile(action='sequence_fund', name=filename, fieldname=funded_fieldname, data=funded_data)
            print '; '.join(r for r in result_fund if r)

            print 'Get started to collect progress data'
            process = ParseProgress()
            process_data, process_fieldname, result_process = process.parse()
            filename = 'Squence_Progress_' + datetime.datetime.now().strftime("%Y-%m-%d") + '.csv'
            gp.writeFile(action='sequence_process', name=filename, fieldname=process_fieldname, data=process_data)
            print '; '.join(r for r in result_process if r)
        else:
            print 'please input yes or no'
            sys.exit(1)
    except:
        print traceback.print_exc(file=sys.stdout)



