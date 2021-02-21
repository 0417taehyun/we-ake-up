import json
import random
import gspread
import requests

from datetime                     import datetime, timedelta
from slacker                      import Slacker
from oauth2client.service_account import ServiceAccountCredentials

from config                       import token, slack_channel, scope


def create_time():
    date = (datetime.today() + timedelta(hours = 9)).strftime("%Y-%m-%d")
    return date


def post_message(content, token = token["Slack"], channel = slack_channel):
    slack      = Slacker(token = token)
    response   = slack.chat.post_message(channel, content, as_user = True)

    return response


def get_worksheet(worksheet, scope = scope, key = token["GoogleSheet"]):
    credential = ServiceAccountCredentials.from_json_keyfile_name("AccessKey.json", scope)
    gc         = gspread.authorize(credential)
    wks        = gc.open_by_key(key).worksheet(worksheet)

    return wks


def get_date():
    wks  = get_worksheet(worksheet = "3기")
    date = 


def get_members():
    wks     = get_worksheet(worksheet = "3기")
    members = [ {"name": name, "github_id": github_id} for name, github_id in wks.get() ]

    return members


def get_issue(url, headers):
    url     += '/issues'
    response = requests.get(url, headers = headers).json()

    return response


def get_comments(url, headers):
    url      += "/comments"
    response  = requests.get(url, headers = headers).json()
    
    return response


def create_issue(url, headers):
    url  = url + '/issues'
    date = create_time()
    body = {
        "title": f"{date} 기상 기상!",
        "body": f"{date} 기상 기상! 아래 코멘트에 미션을 남겨 주세요 :)"
    }
    response  = requests.post(
        url,
        headers = headers,
        data    = json.dumps(body)
    ).json()

    issue_url = response["html_url"]
    content   = f"기상 기상! 어서 {issue_url} 로 가서 미션 완료해주세요 :)"
    slack_res = post_message(content = content)

    return slack_res


def close_issue(url, headers):
    issue_number = get_issue()[-1]["number"]
    url         += f"/issues/{issue_number}"
    body         = {"state": "closed"}

    requests.patch(
        url,
        headers = headers,
        data = json.dumps(body)
    )

    response        = get_comments(url, headers)
    members         = get_members()
    success_members = [ data["user"]["login"] for data in response ]
    penalty_members = [ member["name"] for member in members if not member["github_id"] in success_members ]

    if penalty_members:
        penalty_members = ', '.join(penalty_members)
        content = {
            f"오늘 못 일어난 사람들: {penalty_members}"
        }
    else:
        content = {
            "대박! 오늘은 벌금 낼 사람이 없어요 :)"
        }

    slack_res = post_message(content = content)

    return slack_res


def get_missoin_person():
    members = get_members()
    person  = random.choice(members)["name"]
    content = {
        f"내일 기상 미션을 정해 줄 사람은 바로! {person}"
    }

    slack_res = post_message(content = content)

    return slack_res


def update_sheet():
    pass