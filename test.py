import gspread

from slacker                      import Conversations, Slacker
from oauth2client.service_account import ServiceAccountCredentials
from datetime                     import datetime

from config                       import token

# scope = [
#     "https://spreadsheets.google.com/feeds",
#     "https://www.googleapis.com/auth/drive"
# ]

# credential = ServiceAccountCredentials.from_json_keyfile_name("AccessKey.json", scope)

# gc = gspread.authorize(credential)


# wks = gc.open_by_key("1eNhqCABLRn37xOSj7q0fUEcbRXs3lyu5CDKCTzWMCig").worksheet("3기")

# date = datetime.today().strftime("%m/%d")[1:]

# # print(date)

# d = wks.row_values(1)[2:]

# print(d)

