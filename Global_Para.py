

# global variables
base_url = "https://app.crowdstreet.com"
login_url = "https://app.crowdstreet.com/accounts/login/"
username = "rheazhou@gmail.com"
password = "Crowd1234566$$$"
session = ""

current_campaign_id = 0
funded_campaign_id = 0
isFirstTime = False

First_Run_Funded = "Data Collection/1/1_First Run_Funded/Portal ID_1_First Run_Funded.csv"
First_Run_In_Progress = "Data Collection/1/1_First Run_In Progress/Portal ID_1_First Run_In Progress.csv"
Subsequent_Runs_Funded_File_Template = "Data Collection/1/1_Subsequent Runs_Funded/Portal ID_1_Subsequent Runs_Funded_{date}.csv"
Subsequent_Runs_In_Progress_File_Template = "Data Collection/1/1_Subsequent Runs_InProgress/Portal ID_1_Subsequent Runs_In Progress_{date}.csv"
Documents_In_Progress = "Data Collection/1/1_Documents_In Progress/1.{ID}"
subsequent_runs_funded_folder = "Data Collection/1/1_Subsequent Runs_Funded/"
subsequent_runs_in_progress_folder = "Data Collection/1/1_Subsequent Runs_In Progress/"
First_Run_Funded_folder = "Data Collection/1/1_First Run_Funded/"
First_Run_In_Progress_folder = "Data Collection/1/1_First Run_In Progress/"

funded_variables_anchors = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date',
                    'First_Time(0/1)', 'Funded(0/1)', 'Date Posted', 'Date Funded', '% Funded']

in_process_variables_anchors = ['Portal ID', 'Campaign ID', 'Campaign Name', 'Data Collection Date',
                    'First_Time(0/1)', 'Funded(0/1)', 'Date Posted', '% Funded']

funded_variables_infile = ""
progress_variables_infile = ""
funded_data = ""
progress_data = ""

