import json
import Global_Para as gp
import os.path
import sys
import csv
import datetime

class FileReaderWriter():
    @classmethod
    def readCurrentConfig(cls):
        config_file = open("current_config.json", "r")
        config_dict = json.load(config_file)
        return config_dict

    @classmethod
    def readFundedConfig(cls):
        funded_file = open("funded_config.json", "r")
        funded_dict = json.load(funded_file)
        return funded_dict

    @classmethod
    def readRunFundedProperties(cls):
        file_name = raw_input("please input the Subsequent Runs_Funded file name used as a base\n")
        file_name = gp.subsequent_runs_funded_folder + file_name + ".csv"
        if not os.path.exists(file_name):
            print "Error: cannot find file in Subsequent Runs_Funded Folder"
            print "system exits..."
            sys.exit(1)

        return FileReaderWriter.reader(file_name)

    @classmethod
    def readInProgressProperties(cls):
        file_name = raw_input("please input Subsequent Runs_In Progress file name used as a base\n")
        file_name = gp.subsequent_runs_in_progress_folder + file_name + ".csv"
        if not os.path.exists(file_name):
            print "Error: cannot find file in Subsequent Runs_In Progress Folder"
            print "system exits..."
            sys.exit(1)

        return FileReaderWriter.reader(file_name)

    @classmethod
    def writeInProgressProperties(cls, fieldname, data):
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")
        file_name = gp.Subsequent_Runs_In_Progress_File_Template.replace("{date}", date)
        if os.path.exists(file_name):
            while 1:
                doesReplace = raw_input("There is a same file in folder %s, replace old one?\n"
                                        " Yes: 1, No: 0\n" % gp.subsequent_runs_in_progress_folder)
                if doesReplace == "1":
                    print "replacing the old file...."
                    FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)
                    print "replaced"
                    return
                elif doesReplace == "0":
                    print "do not replace the old file"
                    return
                else:
                    print "please enter 1 for yes, 0 for no."
        else:
            FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)

    @classmethod
    def writeRunsFundedProperties(cls, fieldname, data):
        date = datetime.datetime.now()
        date = date.strftime("%Y-%m-%d")
        file_name = gp.Subsequent_Runs_Funded_File_Template.replace("{date}", date)
        if os.path.exists(file_name):
            while 1:
                doesReplace = raw_input("There is a same file in folder %s, replace old one?\n"
                                        " Yes: 1, No: 0\n" % gp.subsequent_runs_funded_folder)
                if doesReplace == "1":
                    print "replacing the old file...."
                    FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)
                    print "replaced"
                    return
                elif doesReplace == "0":
                    print "do not replace the old file"
                    return
                else:
                    print "please enter 1 for yes, 0 for no."
        else:
            FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)

    @classmethod
    def writeFirstRunFunded(cls, fieldname, data):
        file_name = "Portal ID_1_First Run_Funded.csv"
        if os.path.exists(gp.First_Run_Funded):
            while 1:
                doesReplace = raw_input("There is a same file in folder %s and folder %s, replace old ones?\n"
                                        " Yes: 1, No: 0\n" % (gp.First_Run_Funded_folder, gp.subsequent_runs_funded_folder))
                if doesReplace == "1":
                    print "replace the old files...."
                    FileReaderWriter.writer(file_name=gp.First_Run_Funded, fieldname=fieldname, data=data)
                    file_name = gp.subsequent_runs_funded_folder + file_name
                    FileReaderWriter.writer(file_name=file_name, fieldname=fieldname,data=data)
                    print "replaced"
                    return
                elif doesReplace == "0":
                    print "do not replace the old file"
                    return
                else:
                    print "please enter 1 for yes, 0 for no."
        else:
            FileReaderWriter.writer(file_name=gp.First_Run_Funded, fieldname=fieldname, data=data)
            file_name = gp.subsequent_runs_funded_folder + file_name
            FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)

    @classmethod
    def writeFirstRunInProgress(cls, fieldname, data):
        file_name = "Portal ID_1_First Run_In Progress.csv"
        if os.path.exists(gp.First_Run_In_Progress):
            while 1:
                doesReplace = raw_input("There is a same file in folder %s and folder %s, replace old ones?\n"
                                        " Yes: 1, No: 0\n" % (gp.First_Run_In_Progress_folder, gp.subsequent_runs_in_progress_folder))
                if doesReplace == "1":
                    print "replace the old files...."
                    FileReaderWriter.writer(file_name=gp.First_Run_In_Progress, fieldname=fieldname, data=data)
                    file_name = gp.subsequent_runs_in_progress_folder + file_name
                    FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)
                    print "replaced"
                    return
                elif doesReplace == "0":
                    print "do not replace the old file"
                    return
                else:
                    print "please enter 1 for yes, 0 for no."
        else:
            FileReaderWriter.writer(file_name=gp.First_Run_In_Progress, fieldname=fieldname, data=data)
            file_name = gp.subsequent_runs_in_progress_folder + file_name
            FileReaderWriter.writer(file_name=file_name, fieldname=fieldname, data=data)

    @staticmethod
    def writer(file_name, fieldname, data):
        with open(file_name, "wb") as csvDict:
            writer = csv.DictWriter(csvDict, fieldnames=fieldname)
            writer.writeheader()
            writer.writerows(data)

    @staticmethod
    def reader(file_name):
        with open(file_name, "rb") as csvDict:
            reader = csv.DictReader(csvDict)
            variable_names = reader.fieldnames
            previous_data = []
            for row in reader:
                previous_data.append(row)
        return variable_names, previous_data


