import json
import requests

from worker import create_time, post_message, get_members


def get_issue(url, headers):
    url     += '/issues'
    response = requests.get(url, headers = headers).json()

    return response


def get_comments(url, headers):
    url      += "/comments"
    response  = requests.get(url, headers = headers).json()
    
    return response


def create_wake_up(url, headers):
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