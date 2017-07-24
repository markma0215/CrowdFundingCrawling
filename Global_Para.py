
import time

# global variables
login_url = "https://app.crowdstreet.com/accounts/login/"
username = "rheazhou@gmail.com"
password = "Crowd1234566$$$"
login_cookies = {}

website_structure_has_changed = "website structure has changed"

mandatory_variables = {
    "Portal ID": 1,
    "Campaign Name": None,
    "Data Collection Date": time.strftime("%Y-%m-%d"),
    "Campaign ID": None,
    "First_Time(0/1)": 0,
    "Date Posted": None,
    "Date Funded": None,
    "% Funded": None,
}

funded_variables = {
    "Funded(0/1)": 1,
    "Location": None,
    "Fund Name": None,
    "Funding Amount": None,
    "Num. Investors": None,
    "TARGETED INVESTOR IRR": None,
    "TARGETED EQUITY MULTIPLE": None,
    "TARGETED INVESTMENT PERIOD": None,
    "INVESTMENT PROFILE": None,
    "Closed": None,
    "PROJETED EQUITY MULTIPLE": None,
    "PROJECTED INVESTMENT PERIOD": None,
    "TARGETED AVG. ANNUAL CASH YIELD": None,
    "LOCATION": None
}

processing_variables = {

}