import json
import random
import gspread
import requests

from datetime                     import datetime, timedelta
from slacker                      import Slacker
from oauth2client.service_account import ServiceAccountCredentials

from config                       import token, slack_channel_id, scope


def create_time():
    date = (datetime.today() + timedelta(hours = 9)).strftime("%Y-%m-%d")
    return date


def get_worksheet(worksheet = "3기", scope = scope, key = token["GoogleSheet"]):
    credential = ServiceAccountCredentials.from_json_keyfile_name("AccessKey.json", scope)
    gc         = gspread.authorize(credential)
    wks        = gc.open_by_key(key).worksheet(worksheet)

    return wks


def get_column(cell):
    wks    = get_worksheet()
    column = wks.find(cell).col

    return column


def get_members():
    wks     = get_worksheet()
    column  = get_column("이름")
    members = [ name for name in wks.col_values(column) ]

    return members


def update_sheet():
    pass


def get_slack(token = token["Slack"]):
    slack = Slacker(token)

    return slack


def get_channel_id(channel_name = "we-ake-up-테스트"):
    slack    = get_slack()
    response = slack.conversations.list(limit = 1000)
    channels = response.__dict__["body"]["channels"]

    for channel in channels:
        if channel["name"] == channel_name:
            return channel["id"]

    return response


def post_message(content):
    slack      = get_slack()
    channel_id = get_channel_id()
    response   = slack.chat.post_message(channel_id, content)

    return response


def get_recent_bot_message():
    slack      = get_slack()
    channel_id = get_channel_id()
    response   = slack.conversations.history(channel_id)
    messages   = response.__dict__["body"]["messages"]

    for message in messages:
        try:
            if message["bot_id"]:
                return message["ts"]
        except:
            continue

    return response


def get_user_display_name(user_id):
    slack    = get_slack()
    response = slack.users.profile.get(user = user_id)
    name     = response.__dict__["body"]["profile"]["display_name"]

    return name


def get_success_members():
    slack      = get_slack()
    channel_id = get_channel_id()
    ts         = get_recent_bot_message()
    response   = slack.conversations.replies(channel_id, ts)
    threads    = response.__dict__["body"]["messages"]

    success_members = set()

    for thread in threads:
        try:
            if thread["files"]:
                success_members.add(get_user_display_name(thread["user"]))
        except:
            continue

    return list(success_members)


def get_penalty_members():
    members         = get_members()[1:-1]
    success_members = get_success_members()
    penalty_members = [ member for member in members if not member in success_members ]
    penalty_members = ', '.join(penalty_members)

    if penalty_members:
        content     = f"오늘 못 일어난 사람들: {penalty_members}"
    else:
        content     = "대박! 오늘은 다 일어났어요."

    return content


def get_mission_person():
    members  = get_members()
    person   = random.choice(members)
    content  = f"내일 기상 미션을 정해 줄 사람은 바로! {person}"

    return content