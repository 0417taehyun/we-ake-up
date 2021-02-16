import json
import random
import requests

from datetime import datetime, timedelta
from slacker  import Slacker

from config   import token, members


def create_time():
    date = (datetime.today() + timedelta(hours = 9)).strftime("%Y-%m-%d")
    return date


class Worker():
    slack = Slacker(token = token["Slack"])

    def __init__(self, url, headers):
        self.url     = url
        self.headers = headers


    def get_issues(self):
        url          = self.url + '/issues'
        res          = requests.get(url, headers = self.headers).json()
        return res


    def create_issue(self):
        url  = self.url + '/issues'
        date = create_time()
        body = {
            "title": f"{date} 기상 기상!",
            "body" : f"{date} 기상 기상! 아래 코멘트에 미션을 남겨 주세요 :)"
        }

        res = requests.post(
            url,
            headers = self.headers,
            data    = json.dumps(body)
        ).json()
        
        url = res["html_url"]

        self.slack.chat.post_message(
            "#we-ake-up",
            f"기상 기상! 어서 {url} 로 가서 미션 완료해주세요 :)",
            as_user = True
        )


    def close_issue(self):
        issue_number = self.get_issues()[-1]['number']

        url  = self.url + f'/issues/{issue_number}'
        body = {"state": "closed"}

        requests.patch(
            url,
            headers = self.headers,
            data    = json.dumps(body)
        )

        res = requests.get(
            url + "/comments",
            headers = self.headers
        ).json()

        success_members = [ data["user"]["login"] for data in res ]
        penalty_members = [ member["name"] for member in members if member["github_id"] in success_members ]


        if penalty_members:
            penalty_members = ', '.join(penalty_members)
            self.slack.chat.post_message(
                "#we-ake-up",
                f"오늘 못 일어난 사람들: {penalty_members}"
            )
        else:
            self.slack.chat.post_message(
                "#we-ake-up",
                "대박! 오늘은 벌금 낼 사람이 없어요 :)"
            )

        mission_person = random.choice(members)["name"]

        self.slack.chat.post_message(
            "#we-ake-up",
            f"내일 기상 미션을 정해줄 사람은 바로! {mission_person}"
        )